
import requests, os, sys, jwt, pickle, json, binascii, time, urllib3, base64, datetime, re, socket, threading, ssl, pytz, aiohttp, asyncio
from protobuf_decoder.protobuf_decoder import Parser
from xPARA import *
from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2, sQ_pb2, Team_msg_pb2
from cfonts import render, say
from flask import Flask, request, jsonify
from queue import Queue
import logging

# Configure logging for Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Flask App Setup
app = Flask(__name__)

# Global Variables
Chat_Leave = False
joining_team = False
login_url, ob, version = AuToUpDaTE()

# Command Queue for API requests
command_queue = Queue()

Hr = {
    'User-Agent': Uaa(),
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': ob
}

def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)

async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200:
                return await response.read()
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = version
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0UQgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return await encrypted_proto(string)

async def MajorLogin(payload):
    url = f"{login_url}MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization'] = f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto

async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9:
        headers = '0000000'
    elif uid_length == 8:
        headers = '00000000'
    elif uid_length == 10:
        headers = '000000'
    elif uid_length == 7:
        headers = '000000000'
    else:
        logger.warning('Unexpected UID length')
        headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

class CLIENT:
    def __init__(self):
        self.whisper_writer = None
        self.online_writer = None
        self.uid = None
        self.room_uid = None
        self.response = None
        self.inPuTMsG = None
        self.chat_id = None
        self.data = None
        self.data2 = None
        self.key = None
        self.iv = None
        self.STATUS = None
        self.AutHToKen = None
        self.OnLineiP = None
        self.OnLineporT = None
        self.ChaTiP = None
        self.ChaTporT = None
        self.LoGinDaTaUncRypTinG = None
        self.response = None
        self.uid = None
        self.chat_id = None
        self.XX = None
        self.inPuTMsG = None
        self.insquad = None
        self.sent_inv = None
        self.bot_ready = False
        self.current_squad_owner = None
        self.is_running = False

    async def cHTypE(self, H):
        if not H:
            return 'Squid'
        elif H == 1:
            return 'CLan'
        elif H == 2:
            return 'PrivaTe'

    async def SEndMsG(self, H, message, Uid, chat_id, key, iv):
        TypE = await self.cHTypE(H)
        if TypE == 'Squid':
            msg_packet = await xSEndMsgsQ(message, chat_id, key, iv)
        elif TypE == 'CLan':
            msg_packet = await xSEndMsg(message, 1, chat_id, chat_id, key, iv)
        elif TypE == 'PrivaTe':
            msg_packet = await xSEndMsg(message, 2, Uid, Uid, key, iv)
        return msg_packet

    async def SEndPacKeT(self, OnLinE, ChaT, TypE, PacKeT):
        if TypE == 'ChaT' and ChaT:
            self.whisper_writer.write(PacKeT)
            await self.whisper_writer.drain()
        elif TypE == 'OnLine':
            self.online_writer.write(PacKeT)
            await self.online_writer.drain()
        else:
            logger.error('Unsupported packet type')

    async def process_api_commands(self):
        """Process commands from API queue"""
        while self.is_running:
            try:
                if not command_queue.empty():
                    command = command_queue.get()
                    command_type = command.get('type')
                    
                    if command_type == 'join_and_emote':
                        team_code = command.get('team_code')
                        uids = command.get('uids', [])
                        emote_id = command.get('emote_id')
                        
                        # Join team using code
                        logger.info(f"[API] Joining team with code: {team_code}")
                        join_packet = await GenJoinSquadsPacket(team_code, self.key, self.iv)
                        await self.SEndPacKeT(self.whisper_writer, self.online_writer, 'OnLine', join_packet)
                        
                        # Ultra-fast join wait (0.4 seconds)
                        await asyncio.sleep(0.4)
                        
                        # Prepare all emote packets simultaneously
                        emote_packets = []
                        for uid in uids:
                            if uid:
                                logger.info(f"[API] Preparing emote {emote_id} for UID: {uid}")
                                emote_packet = await Emote_k(uid, emote_id, self.key, self.iv)
                                emote_packets.append(emote_packet)
                        
                        # Send ALL emote packets at once (no delays between)
                        for packet in emote_packets:
                            self.online_writer.write(packet)
                        await self.online_writer.drain()  # Single drain call
                        logger.info(f"[API] Sent {len(emote_packets)} emotes simultaneously")
                        
                        # Minimal leave time
                        await asyncio.sleep(0.1)
                        
                        # Leave squad after emotes
                        leave_packet = await ExiT(None, self.key, self.iv)
                        await self.SEndPacKeT(self.whisper_writer, self.online_writer, 'OnLine', leave_packet)
                        logger.info(f"[API] Command completed in ~0.5 seconds")
                        
            except Exception as e:
                logger.error(f"[API] Error processing command: {e}")
            
            await asyncio.sleep(0.1)

    async def TcPOnLine(self, ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
        global Chat_Leave, joining_team
        while self.is_running:
            try:
                reader, writer = await asyncio.open_connection(ip, int(port))
                self.online_writer = writer
                bytes_payload = bytes.fromhex(AutHToKen)
                self.online_writer.write(bytes_payload)
                await self.online_writer.drain()
                
                logger.info(f"[Online] Connected to {ip}:{port}")
                
                while self.is_running:
                    self.data2 = await reader.read(9999)
                    data2 = self.data2
                    if not data2:
                        break

                    if self.data2:
                        # Handle squad invites (auto-refuse and send back)
                        if self.data2.hex().startswith("0500") and self.insquad is None and joining_team == False:
                            packet = await DeCode_PackEt(self.data2.hex()[10:])
                            packet = json.loads(packet)
                            try:
                                invite_uid = packet['5']['data']['2']['data']['1']['data']
                                squad_owner = packet['5']['data']['1']['data']
                                squad_code = packet['5']['data']['8']['data']
                                RefUse = await RedZedRefuse(squad_owner, invite_uid, key, iv)
                                await self.SEndPacKeT(self.whisper_writer, self.online_writer, 'OnLine', RefUse)
                                SendInv = await RedZed_SendInv(invite_uid, key, iv)
                                await self.SEndPacKeT(self.whisper_writer, self.online_writer, 'OnLine', SendInv)
                                self.insquad = False
                            except:
                                continue
                            
                            if self.insquad == False:
                                Join = await RedZedAccepted(squad_owner, squad_code, key, iv)
                                await self.SEndPacKeT(self.whisper_writer, self.online_writer, 'OnLine', Join)
                                self.insquad = True

                        # Handle team join confirmation
                        if self.data2.hex().startswith('0500') and len(self.data2.hex()) > 1000 and joining_team:
                            try:
                                packet = await DeCode_PackEt(self.data2.hex()[10:])
                                packet = json.loads(packet)
                                OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(packet)
                                self.current_squad_owner = OwNer_UiD
                                JoinCHaT = await AutH_Chat(3, OwNer_UiD, CHaT_CoDe, key, iv)
                                await self.SEndPacKeT(self.whisper_writer, self.online_writer, 'ChaT', JoinCHaT)
                                logger.info(f"[API] Successfully joined squad, Owner UID: {OwNer_UiD}")
                            except Exception as e:
                                logger.error(f"[API] Error joining squad chat: {e}")
                        
                        joining_team = False

                if self.whisper_writer is not None:
                    try:
                        self.whisper_writer.close()
                        await self.whisper_writer.wait_closed()
                    except Exception as e:
                        logger.error(f"Error closing whisper_writer: {e}")
                    finally:
                        self.whisper_writer = None

                if self.online_writer is not None:
                    try:
                        self.online_writer.close()
                        await self.online_writer.wait_closed()
                    except Exception as e:
                        logger.error(f"Error closing online_writer: {e}")
                    finally:
                        self.online_writer = None

                self.insquad = None

            except Exception as e:
                logger.error(f"- Error With {ip}:{port} - {e}")
                self.online_writer = None
            await asyncio.sleep(reconnect_delay)

    async def TcPChaT(self, ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, reconnect_delay=0.5):
        global Chat_Leave, joining_team
        while self.is_running:
            try:
                reader, writer = await asyncio.open_connection(ip, int(port))
                self.whisper_writer = writer
                bytes_payload = bytes.fromhex(AutHToKen)
                self.whisper_writer.write(bytes_payload)
                await self.whisper_writer.drain()
                ready_event.set()
                
                logger.info(f"[Chat] Connected to {ip}:{port}")
                
                if LoGinDaTaUncRypTinG.Clan_ID:
                    clan_id = LoGinDaTaUncRypTinG.Clan_ID
                    clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                    logger.info('\n - Bot is in Clan!')
                    logger.info(f' - Clan UID: {clan_id}')
                    pK = await AuthClan(clan_id, clan_compiled_data, key, iv)
                    if self.whisper_writer:
                        self.whisper_writer.write(pK)
                        await self.whisper_writer.drain()
                
                self.bot_ready = True
                logger.info("[Bot] Ready to receive API commands!")
                
                while self.is_running:
                    self.data = await reader.read(9999)
                    data = self.data
                    if not data:
                        break

                if self.whisper_writer is not None:
                    try:
                        self.whisper_writer.close()
                        await self.whisper_writer.wait_closed()
                    except Exception as e:
                        logger.error(f"Error closing whisper_writer: {e}")
                    finally:
                        self.whisper_writer = None

                if self.online_writer is not None:
                    try:
                        self.online_writer.close()
                        await self.online_writer.wait_closed()
                    except Exception as e:
                        logger.error(f"Error closing online_writer: {e}")
                    finally:
                        self.online_writer = None

                self.insquad = None

            except Exception as e:
                logger.error(f"Error {ip}:{port} - {e}")
                self.whisper_writer = None
            await asyncio.sleep(reconnect_delay)

    async def start(self):
        """Start the bot client"""
        self.is_running = True
        Uid, Pw = '4232977194','JOBAYAR_CODX-DJJWHJGQB'
        
        open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
        if not open_id or not access_token:
            logger.error("Error - Invalid Account")
            return None

        PyL = await EncRypTMajoRLoGin(open_id, access_token)
        MajoRLoGinResPonsE = await MajorLogin(PyL)
        if not MajoRLoGinResPonsE:
            logger.error("Target Account => Banned / Not Registered!")
            return None

        MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
        UrL = MajoRLoGinauTh.url
        ToKen = MajoRLoGinauTh.token
        self.JWT = ToKen
        TarGeT = MajoRLoGinauTh.account_uid
        self.key = MajoRLoGinauTh.key
        self.iv = MajoRLoGinauTh.iv
        timestamp = MajoRLoGinauTh.timestamp

        LoGinDaTa = await GetLoginData(UrL, PyL, ToKen)
        if not LoGinDaTa:
            logger.error("Error - Getting Ports From Login Data!")
            return None
        LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
        ReGioN = LoGinDaTaUncRypTinG.Region
        AccountName = LoGinDaTaUncRypTinG.AccountName
        OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
        ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
        self.OnLineiP, self.OnLineporT = OnLinePorTs.split(":")
        ChaTiP, ChaTporT = ChaTPorTs.split(":")
        AutHToKen = await xAuThSTarTuP(int(TarGeT), ToKen, int(timestamp), self.key, self.iv)
        ready_event = asyncio.Event()

        task1 = asyncio.create_task(self.TcPChaT(ChaTiP, ChaTporT, AutHToKen, self.key, self.iv, LoGinDaTaUncRypTinG, ready_event))
        await ready_event.wait()
        await asyncio.sleep(1)
        task2 = asyncio.create_task(self.TcPOnLine(self.OnLineiP, self.OnLineporT, self.key, self.iv, AutHToKen))
        task3 = asyncio.create_task(self.process_api_commands())
        
        logger.info(render('REDZED API', colors=['white', 'red'], align='center'))
        logger.info(f" - Server Login URL => {login_url} | Server URL => {UrL}\n")
        logger.info(f" - Game Status > Good | OB => {ob} | Version => {version}\n")
        logger.info(f" - Bot Starting on Target: {AccountName}, UID: {TarGeT} | Region => {ReGioN}\n")
        logger.info(f" - Bot Status > Good | Online!\n")
        logger.info(f" - API Server running on Render\n")
        logger.info(f" - Ultra-Optimized Timing: Join=0.4s, Emotes=Simultaneous, Leave=0.1s\n")

        await asyncio.gather(task1, task2, task3)

    async def stop(self):
        """Stop the bot client"""
        self.is_running = False
        if self.whisper_writer:
            self.whisper_writer.close()
        if self.online_writer:
            self.online_writer.close()

# Global client instance
client = CLIENT()

# Flask API Routes
@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Free Fire Emote Bot API - Running on Render",
        "bot_ready": client.bot_ready,
        "timing_info": {
            "join_wait": "0.4 seconds",
            "emote_delay": "Simultaneous for all UIDs",
            "leave_wait": "0.1 seconds",
            "total_approx": "~0.5 seconds for any number of UIDs"
        },
        "endpoints": {
            "join": "/join?tc=TEAMCODE&uid1=UID1&uid2=UID2&uid3=UID3&uid4=UID4&uid5=UID5&emote_id=EMOTE_ID",
            "status": "/status"
        }
    })

@app.route('/join')
def join_and_emote():
    """
    Join team and perform emotes
    Example: /join?tc=ABC123&uid1=123456789&uid2=987654321&emote_id=909000001
    """
    try:
        team_code = request.args.get('tc')
        emote_id = request.args.get('emote_id', '909000001')
        
        # Collect all UIDs
        uids = []
        for i in range(1, 6):
            uid = request.args.get(f'uid{i}')
            if uid:
                try:
                    uids.append(int(uid))
                except ValueError:
                    pass
        
        if not team_code:
            return jsonify({
                "status": "error",
                "message": "Team code (tc) is required"
            }), 400
        
        if not uids:
            return jsonify({
                "status": "error",
                "message": "At least one UID is required (uid1, uid2, etc.)"
            }), 400
        
        if not client.bot_ready:
            return jsonify({
                "status": "error",
                "message": "Bot is not ready yet. Please wait."
            }), 503
        
        # Add command to queue
        command_queue.put({
            'type': 'join_and_emote',
            'team_code': team_code,
            'uids': uids,
            'emote_id': int(emote_id)
        })
        
        return jsonify({
            "status": "success",
            "message": "Command queued successfully",
            "data": {
                "team_code": team_code,
                "uids": uids,
                "emote_id": emote_id,
                "estimated_time": "~0.5 seconds"
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/status')
def status():
    """Check bot status"""
    return jsonify({
        "status": "online" if client.bot_ready else "starting",
        "bot_ready": client.bot_ready,
        "connections": {
            "online": client.online_writer is not None,
            "chat": client.whisper_writer is not None
        },
        "timing_optimized": True
    })

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({"status": "healthy", "bot_running": client.is_running})

def run_flask():
    """Run Flask app"""
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

async def main():
    """Main async function to run everything"""
    # Start Flask server in background thread
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info(f"[Flask] API server starting on port {os.environ.get('PORT', 5000)}")
    
    # Wait for Flask to start
    await asyncio.sleep(2)
    
    # Start the bot
    while True:
        try:
            await client.start()
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            await asyncio.sleep(10)  # Wait before restarting

if __name__ == '__main__':
    # For Render deployment
    asyncio.run(main())
