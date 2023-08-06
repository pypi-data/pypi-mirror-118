import os
import sys
import asyncio
import aiofiles
import aiohttp
import uvicorn
import base64
import subprocess
from pytube import YouTube
from pytube.extract import apply_descrambler, apply_signature
from urllib.parse import parse_qs
from pytube import YouTube, extract, __js_url__
from mutagen.mp4 import MP4, MP4Cover
from mutagen.oggopus import OggOpus
from mutagen.flac import Picture
from io import BytesIO
from PIL import Image
from json import dumps, loads
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

VERCEL = False
FFMPEG_COMMAND = 'ffmpeg -i "{track}.webm" -vn -c:a copy -- {track}.ogg'


class Extractor(YouTube):
    def __init__(self):
        self._js_url = None
        self._js = None
        self.stream_urls = {}

    async def get_javascript(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.youtube.com/watch') as response:
                watchHTML = await response.text()
                loop = asyncio.get_event_loop()
                self._js_url = await loop.run_in_executor(None, extract.js_url, watchHTML)
                if __js_url__ != self._js_url:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(self._js_url) as response:
                            self._js = await response.text()

    async def get_stream_urls(self, response_dict):
        self._player_response = {'player_response': response_dict}
        if not response_dict['streamingData']:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post('https://youtube.com/get_video_info',
                                            params={
                                                'video_id': response_dict['videoDetails']['videoId'],
                                                'eurl': f'https://youtube.googleapis.com/v/{response_dict["videoDetails"]["videoId"]}',
                                                'sts': None,
                                            },
                                            timeout=None) as response:
                        self._player_response['player_response'] = await loads(parse_qs(await response.text())['player_response'][0])
            except:
                raise Exception('COULD_NOT_MAKE_REQUEST')
        self.video_id = response_dict['videoDetails']['videoId']
        await self._decipher()
        return self.stream_urls

    async def _decipher(self, retry: bool = False):
        if not self._js or retry:
            await self.get_javascript()
        try:
            self.stream_urls.clear()
            loop = asyncio.get_event_loop()
            streams: list[dict] = await loop.run_in_executor(None, apply_descrambler, self._player_response['player_response']['streamingData'])
            await loop.run_in_executor(None, apply_signature, streams, self._player_response, self._js)
            for stream in streams:
                self.stream_urls[stream['itag']] = stream['url']
        except:
            await self._decipher(retry=True)


track_responses = {}
app: FastAPI = FastAPI()
app.mount(
    '/tracks', StaticFiles(directory='/tmp' if VERCEL else 'tracks'), name='/tmp' if VERCEL else 'tracks')
extractor: Extractor = Extractor()


@app.on_event('startup')
async def startup():
    try:
        await extractor.get_javascript()
        print('START_SUCCESS')
        sys.stdout.flush()
    except:
        print('START_FAILURE')
        sys.stdout.flush()


@app.get('/track_search')
async def search(query):
    async with aiohttp.ClientSession() as session:
        async with session.post('https://music.youtube.com/youtubei/v1/search',
                                params={
                                    'key': 'AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30'},
                                headers={
                                    'accept': '*/*',
                                    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
                                    'content-type': 'application/json',
                                    'dpr': '2',
                                    'sec-ch-ua-arch': '',
                                    'sec-fetch-dest': 'empty',
                                    'sec-fetch-mode': 'same-origin',
                                    'sec-fetch-site': 'same-origin',
                                    'x-origin': 'https://music.youtube.com',
                                    'x-youtube-client-name': '67',
                                    'x-youtube-client-version': '1.20210823.00.00',
                                },
                                json={
                                    'query': query,
                                    'params': 'EgWKAQIIAWoMEAMQBBAOEAoQBRAJ',
                                    'context': {
                                        'client': {
                                            'clientName': 'WEB_REMIX',
                                            'clientVersion': '0.1',
                                            'newVisitorCookie': True,
                                        },
                                        'user': {
                                            'lockedSafetyMode': False,
                                        }
                                    }
                                }) as response:
            response_dict = (await response.json())
            if 'tabbedSearchResultsRenderer' in response_dict['contents']:
                results = response_dict['contents']['tabbedSearchResultsRenderer']['tabs'][0]['tabRenderer']['content']
            else:
                results = response_dict['contents']
            results = results['sectionListRenderer']['contents'][0]['musicShelfRenderer']['contents']
            search_result: list[dict] = []
            for raw_track in results:
                raw_track = raw_track['musicResponsiveListItemRenderer']
                try:
                    track = {
                        'track_id': raw_track['flexColumns'][0]['musicResponsiveListItemFlexColumnRenderer']['text']['runs'][0]['navigationEndpoint']['watchEndpoint']['videoId'],
                        'track_name': raw_track['flexColumns'][0]['musicResponsiveListItemFlexColumnRenderer']['text']['runs'][0]['text'],
                        'track_subtitle': ''.join(map(lambda object: object['text'], raw_track['flexColumns'][1]['musicResponsiveListItemFlexColumnRenderer']['text']['runs'])),
                        'track_album_art': raw_track['thumbnail']['musicThumbnailRenderer']['thumbnail']['thumbnails'][-1]['url'],
                        'album_id': raw_track['menu']['menuRenderer']['items'][-3]['menuNavigationItemRenderer']['navigationEndpoint']['browseEndpoint']['browseId'],
                        'artist_id': raw_track['menu']['menuRenderer']['items'][-2]['menuNavigationItemRenderer']['navigationEndpoint']['browseEndpoint']['browseId'],
                    }
                except:
                    pass
                search_result.append(track)
            return Response(dumps(search_result, indent=4), 200)


@app.get('/track_stream')
async def track(track_id, itag: int = 251):
    if track_id in track_responses:
        response_dict = track_responses[track_id]
    else:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://www.youtube.com/watch',
                                    params={
                                        'v': track_id,
                                        'pbj': 1,
                                    }) as response:
                response_dict = (await response.json())[2]['playerResponse']
                track_responses[track_id] = response_dict
    streams = await extractor.get_stream_urls(response_dict)
    return RedirectResponse(streams[itag])


@app.get('/track_data')
async def track(track_id):
    if track_id in track_responses:
        response_dict = track_responses[track_id]
    else:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://www.youtube.com/watch',
                                    params={
                                        'v': track_id,
                                        'pbj': 1,
                                    }) as response:
                response_dict = (await response.json())[2]['playerResponse']
                track_responses[track_id] = response_dict
    description: list[str] = response_dict['videoDetails']['shortDescription'].split(
        '\n\n')
    track = {
        'track_id': track_id,
        'track_name': response_dict['videoDetails']['title'],
        'track_duration': int(response_dict['streamingData']['adaptiveFormats'][0]['approxDurationMs']),
        'track_artists': [
            artist for artist in description[1].split(' · ')[1:]
        ],
        'album_name': description[2].strip(),
        'album_artist': [
            artist for artist in description[1].split(' · ')[1:]
        ][0],
        'track_copyright': description[3],
        'track_year': (
            None
            if len(description) < 5
            else description[4].replace('Released on: ', '')
        ).split('-')[0],
        'streams': await extractor.get_stream_urls(response_dict)
    }
    return Response(dumps(track, indent=4))


@app.get('/track_download')
async def track(track_id, itag: int = 140):
    if track_id in track_responses:
        response_dict = track_responses[track_id]
    else:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://www.youtube.com/watch',
                                    params={
                                        'v': track_id,
                                        'pbj': 1,
                                    }) as response:
                response_dict = (await response.json())[2]['playerResponse']
                track_responses[track_id] = response_dict
    if not (os.path.exists(f'{os.path.abspath("/tmp" if VERCEL else "tracks")}/{track_id}.m4a') and itag == 140) or not (os.path.exists(f'{os.path.abspath("/tmp" if VERCEL else "tracks")}/{track_id}.m4a') and itag == 251):
        description: list[str] = response_dict['videoDetails']['shortDescription'].split(
            '\n\n')
        track = {
            'track_id': track_id,
            'track_name': response_dict['videoDetails']['title'],
            'track_duration': int(response_dict['streamingData']['adaptiveFormats'][0]['approxDurationMs']),
            'track_artists': [
                artist for artist in description[1].split(' · ')[1:]
            ],
            'album_name': description[2].strip(),
            'album_artist': [
                artist for artist in description[1].split(' · ')[1:]
            ][0],
            'track_copyright': description[3],
            'track_year': (
                None
                if len(description) < 5
                else description[4].replace('Released on: ', '')
            ).split('-')[0],
        }
        streams = await extractor.get_stream_urls(response_dict)
        async with aiohttp.ClientSession() as session:
            async with session.get(streams[itag],
                                   headers={'Range': 'bytes=0-'}) as response:
                track_responses[track_id] = response_dict
                if itag == 140:
                    async with aiofiles.open(f'{os.path.abspath("/tmp" if VERCEL else "tracks")}/{track_id}.m4a', 'wb') as file:
                        await file.write(await response.read())
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f'https://img.youtube.com/vi/{track_id}/maxresdefault.jpg') as response:
                                cover_bytes = BytesIO()
                                cover_image = Image.open(
                                    BytesIO(await response.read())).crop((280, 0, 1000, 720))
                                cover_image.save(
                                    cover_bytes, format='JPEG')
                                audio_file = MP4(
                                    f'{os.path.abspath("/tmp" if VERCEL else "tracks")}/{track_id}.m4a')
                                cover = MP4Cover(
                                    cover_bytes.getvalue(), imageformat=MP4Cover.FORMAT_JPEG)
                                audio_file['covr'] = [cover]
                                audio_file['\xa9nam'] = track['track_name']
                                audio_file['\xa9alb'] = track['album_name']
                                audio_file['\xa9ART'] = '/'.join(
                                    track['track_artists'])
                                audio_file['aART'] = track['album_artist']
                                audio_file['\xa9day'] = track['track_year']
                                audio_file['\xa9cmt'] = f'https://music.youtube.com/watch?v={track_id}'
                                audio_file['cprt'] = track['track_copyright']
                                audio_file.save()
                elif itag == 251:
                    async with aiofiles.open(f'{os.path.abspath("/tmp" if VERCEL else "tracks")}/{track_id}.webm', 'wb') as file:
                        await file.write(await response.read())
                        process = subprocess.Popen(
                            FFMPEG_COMMAND.format(
                                track='/tmp' if VERCEL else 'tracks' + '/' + track_id),
                            shell=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.PIPE,
                        )
                        while process.poll() is None:
                            await asyncio.sleep(0.1)
                        _, stderr = process.communicate()
                        stderr = stderr.decode()
                        if process.poll() != 0:
                            print('[stderr]', stderr)
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f'https://img.youtube.com/vi/{track_id}/maxresdefault.jpg') as response:
                                cover_bytes = BytesIO()
                                cover_image = Image.open(
                                    BytesIO(await response.read())).crop((280, 0, 1000, 720))
                                cover_image.save(
                                    cover_bytes, format='JPEG')
                                audio_file = OggOpus(
                                    f'{os.path.abspath("/tmp" if VERCEL else "tracks")}/{track_id}.ogg')
                                cover = Picture()
                                cover.data = cover_bytes.getvalue()
                                cover.type = 3
                                cover.desc = 'Cover (front)'
                                cover.mime = 'image/jpeg'
                                cover.width = 720
                                cover.height = 720
                                encoded_data = base64.b64encode(
                                    cover.write())
                                vcomment_value = encoded_data.decode("ascii")
                                audio_file['metadata_block_picture'] = [
                                    vcomment_value]
                                audio_file['title'] = [track['track_name']]
                                audio_file['album'] = [track['album_name']]
                                audio_file['artist'] = [
                                    '/'.join(track['track_artists'])]
                                audio_file['albumartist'] = [
                                    track['album_artist']]
                                audio_file['date'] = [track['track_year']]
                                audio_file.save()
    return RedirectResponse(f'{"/tmp" if VERCEL else "tracks"}/{track_id}.{"m4a" if itag == 140 else "ogg"}')


def main():
    if not os.path.exists('/tmp' if VERCEL else 'tracks'):
        os.mkdir('/tmp' if VERCEL else 'tracks')
    uvicorn.run('yt-music-headless:app',
                port=int(sys.argv[1]), log_level='critical')


if __name__ == '__main__':
    main()
