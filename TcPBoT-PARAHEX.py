import requests, os, sys, jwt, pickle, json, binascii, time, urllib3, base64, datetime, re, socket, threading, ssl, pytz, aiohttp, asyncio, random
from protobuf_decoder.protobuf_decoder import Parser
from xPARA import *
from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Lock
from Pb2 import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2, sQ_pb2, Team_msg_pb2
from cfonts import render, say
from flask import Flask, request, jsonify
from collections import deque
import logging
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

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

# UNLIMITED Command Queue
command_queue = deque()  # Unlimited size
queue_lock = Lock()
currently_processing = False
processed_commands = 0

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
        self.command_history = []
        self.successful_commands = 0
        self.failed_commands = 0

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

    async def execute_single_command(self, command):
        """Execute a single command from queue"""
        global currently_processing, processed_commands
        
        try:
            team_code = command.get('team_code')
            uids = command.get('uids', [])
            emote_id = command.get('emote_id')
            
            logger.info(f"[QUEUE] Executing command: Team={team_code}, UIDs={len(uids)}")
            
            # 1. JOIN TEAM - 0.13 seconds (UPDATED)
            join_packet = await GenJoinSquadsPacket(team_code, self.key, self.iv)
            await self.SEndPacKeT(self.whisper_writer, self.online_writer, 'OnLine', join_packet)
            await asyncio.sleep(0.13)  # Join wait - UPDATED to 0.13s
            
            # 2. EXECUTE ALL EMOTES SIMULTANEOUSLY
            success_emotes = 0
            for uid in uids:
                if uid:
                    try:
                        emote_packet = await Emote_k(uid, emote_id, self.key, self.iv)
                        self.online_writer.write(emote_packet)
                        success_emotes += 1
                    except Exception as e:
                        logger.error(f"[QUEUE] Error creating emote for UID {uid}: {e}")
            
            # Send all emote packets at once
            await self.online_writer.drain()
            
            # 3. LEAVE TEAM - 0.05 seconds
            await asyncio.sleep(0.05)  # Leave wait
            leave_packet = await ExiT(None, self.key, self.iv)
            await self.SEndPacKeT(self.whisper_writer, self.online_writer, 'OnLine', leave_packet)
            
            # Track statistics
            self.successful_commands += 1
            processed_commands += 1
            
            self.command_history.append({
                'time': datetime.now().isoformat(),
                'team_code': team_code,
                'uids_count': len(uids),
                'emote_id': emote_id,
                'successful_emotes': success_emotes,
                'status': 'success',
                'total_time': '~0.18 seconds'
            })
            
            # Keep only last 10 commands
            if len(self.command_history) > 10:
                self.command_history = self.command_history[-10:]
            
            logger.info(f"[QUEUE] Command completed in ~0.18 seconds")
            logger.info(f"[QUEUE] Remaining in queue: {len(command_queue)} commands")
            
            return True, f"Executed {success_emotes} emotes successfully"
            
        except Exception as e:
            logger.error(f"[QUEUE] Error executing command: {e}")
            self.failed_commands += 1
            
            self.command_history.append({
                'time': datetime.now().isoformat(),
                'team_code': command.get('team_code', 'N/A'),
                'status': 'failed',
                'error': str(e)
            })
            
            return False, f"Error: {str(e)}"

    async def process_queue_continuously(self):
        """Continuously process queue - ONE command at a time"""
        global currently_processing, processed_commands
        
        while self.is_running:
            try:
                with queue_lock:
                    if command_queue and not currently_processing:
                        # Take the first command from queue
                        command = command_queue[0]  # Peek at first
                        currently_processing = True
                    else:
                        command = None
                
                if command:
                    # Execute the command
                    success, message = await self.execute_single_command(command)
                    
                    # Remove the command from queue AFTER execution
                    with queue_lock:
                        if command_queue and command_queue[0] == command:
                            command_queue.popleft()  # Remove the executed command
                        currently_processing = False
                    
                    # MINIMAL gap between commands - 0.08 seconds
                    await asyncio.sleep(0.08)
                    
                else:
                    # No commands to process
                    await asyncio.sleep(0.05)
                    
            except Exception as e:
                logger.error(f"[QUEUE] Error in queue processor: {e}")
                with queue_lock:
                    currently_processing = False
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
        # CHANGE THESE CREDENTIALS TO YOUR OWN
        Uid, Pw = '4357855347','ZX-BOSS_ZX_BOSS_S2D6W_8_level_id_genarator'
        
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
        task3 = asyncio.create_task(self.process_queue_continuously())
        
        logger.info(render('ZX API', colors=['red', 'blue'], align='center'))
        logger.info(f" - Bot Starting on Target: {AccountName}, UID: {TarGeT} | Region => {ReGioN}")
        logger.info(f" - Bot Status > Good | Online!")
        logger.info(f" - Queue System: UNLIMITED (Execute → Remove → Next)")
        logger.info(f" - ⚡ ULTRA-FAST TIMING:")
        logger.info(f"      Join Team: 0.13 seconds")
        logger.info(f"      Execute Emotes: Simultaneous")
        logger.info(f"      Leave Team: 0.05 seconds")
        logger.info(f"      Gap Between Commands: 0.08 seconds")
        logger.info(f"      Total per Command: ~0.26 seconds")
        logger.info(f" - DEVELOPER: ZX BOSS 💥 ⁉️ ☠️")
        logger.info(f" - TELEGRAM: @ZXBOSS1 | CHANNEL: ZXOFFLCIAL11")

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
    with queue_lock:
        queue_size = len(command_queue)
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ZX BOSS FREE FIRE API</title>
        <style>
            body {
                background: linear-gradient(135deg, #000000, #8B0000);
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
            }
            .container {
                background: rgba(0, 0, 0, 0.7);
                border-radius: 15px;
                padding: 30px;
                margin: 0 auto;
                max-width: 600px;
                border: 2px solid #FF0000;
            }
            h1 {
                color: #FF0000;
                font-size: 2.5em;
                margin-bottom: 20px;
                text-shadow: 0 0 10px #FF0000;
            }
            .emoji {
                font-size: 2em;
            }
            .contact {
                background: rgba(255, 0, 0, 0.2);
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .endpoint {
                background: rgba(255, 255, 255, 0.1);
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
                text-align: left;
                font-family: monospace;
            }
            .status {
                color: #00FF00;
                font-weight: bold;
            }
            .stats {
                background: rgba(0, 255, 0, 0.1);
                padding: 10px;
                border-radius: 10px;
                margin: 15px 0;
            }
            .queue-status {
                margin: 15px 0;
                padding: 10px;
                border-radius: 5px;
                background: rgba(255, 255, 0, 0.1);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="emoji">💥 ⁉️ ☠️</div>
            <h1>API IS WORKING</h1>
            
            <div class="contact">
                <h2>DEVELOPER: ZX BOSS 💥 ⁉️ ☠️</h2>
                <p>TELEGRAM CONTACT: @ZXBOSS1</p>
                <p>TELEGRAM CHANNEL: ZXOFFLCIAL11</p>
            </div>
            
            <div class="stats">
                <h3>BOT STATS</h3>
                <p>Status: <span class="status">{}</span></p>
                <p>Queue Size: <span class="status">{}</span></p>
                <p>Processing Now: <span class="status">{}</span></p>
                <p>Successful: {} | Failed: {}</p>
                <p>Total Processed: {}</p>
            </div>
            
            <h3>API ENDPOINTS:</h3>
            <div class="endpoint">
                <strong>Join Team & Emote:</strong><br>
                GET /join?tc=TEAMCODE&uid1=UID1&uid2=UID2&uid3=UID3&uid4=UID4&uid5=UID5&emote_id=EMOTE_ID
            </div>
            <div class="endpoint">
                <strong>Check Status:</strong><br>
                GET /status
            </div>
            <div class="endpoint">
                <strong>Health Check:</strong><br>
                GET /health
            </div>
            
            <p style="margin-top: 30px; color: #888;">
                ⚡ Timing: Join=0.13s | Emotes=Simultaneous | Leave=0.05s | Gap=0.08s
            </p>
        </div>
    </body>
    </html>
    '''.format(
        "READY" if client.bot_ready else "STARTING",
        queue_size,
        "YES" if currently_processing else "NO",
        client.successful_commands,
        client.failed_commands,
        processed_commands
    )

@app.route('/join')
def join_and_emote():
    """
    Join team and perform emotes
    Returns EXACT format as requested
    """
    try:
        team_code = request.args.get('tc')
        emote_id = request.args.get('emote_id', '909000001')
        
        if not team_code:
            return jsonify({
                "status": "error",
                "message": "Team code (tc) is required"
            }), 400
        
        # Collect all UIDs
        uids = []
        for i in range(1, 6):
            uid = request.args.get(f'uid{i}')
            if uid:
                try:
                    uids.append(int(uid))
                except ValueError:
                    return jsonify({
                        "status": "error",
                        "message": f"UID{i} must be a valid number"
                    }), 400
        
        if not uids:
            return jsonify({
                "status": "error",
                "message": "At least one UID is required (uid1, uid2, etc.)"
            }), 400
        
        if not client.bot_ready:
            return jsonify({
                "status": "error",
                "message": "Bot is not ready yet. Please wait 5-10 seconds."
            }), 503
        
        # Create command
        command = {
            'type': 'join_and_emote',
            'team_code': team_code,
            'uids': uids,
            'emote_id': int(emote_id),
            'timestamp': datetime.now().isoformat(),
            'id': int(time.time() * 1000)  # Unique ID
        }
        
        # Add to UNLIMITED queue
        with queue_lock:
            command_queue.append(command)
            queue_size = len(command_queue)
        
        # Calculate estimated time (0.26 seconds per command in queue)
        estimated_seconds = queue_size * 0.26
        # Format as requested: "~[time]seconds"
        estimated_time_str = f"~{estimated_seconds:.1f}seconds"
        
        # ALWAYS return "Command queued successfully" message
        return jsonify({
            "status": "success",
            "message": "Command queued successfully",
            "data": {
                "team_code": team_code,
                "uids": uids,
                "emote_id": emote_id,
                "estimated_time": estimated_time_str
            }
        })
        
    except Exception as e:
        logger.error(f"Error in /join endpoint: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/status')
def status():
    """Check bot status"""
    with queue_lock:
        queue_size = len(command_queue)
    
    return jsonify({
        "status": "online",
        "bot_ready": client.bot_ready,
        "queue_system": {
            "type": "UNLIMITED (execute → remove → next)",
            "current_size": queue_size,
            "currently_processing": currently_processing,
            "processed_total": processed_commands,
            "successful": client.successful_commands,
            "failed": client.failed_commands
        },
        "timing": {
            "join_wait": "0.13 seconds",
            "emote_execution": "SIMULTANEOUS",
            "leave_wait": "0.05 seconds",
            "gap_between_commands": "0.08 seconds",
            "total_cycle_per_command": "~0.26 seconds"
        },
        "performance": {
            "estimated_commands_per_minute": "~230 commands"
        },
        "developer": "ZX BOSS 💥 ⁉️ ☠️",
        "contact": "@ZXBOSS1",
        "channel": "ZXOFFLCIAL11"
    })

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    with queue_lock:
        queue_size = len(command_queue)
    
    return jsonify({
        "status": "healthy", 
        "bot_running": client.is_running,
        "bot_ready": client.bot_ready,
        "queue": {
            "size": queue_size,
            "processing": currently_processing
        },
        "timestamp": datetime.now().isoformat(),
        "message": "ZX BOSS API - Running 💥"
    })

@app.route('/queue')
def queue_status():
    """Show queue status (admin)"""
    with queue_lock:
        queue_list = list(command_queue)
    
    return jsonify({
        "queue_size": len(queue_list),
        "currently_processing": currently_processing,
        "queued_commands": [
            {
                "team_code": cmd.get('team_code'),
                "uids_count": len(cmd.get('uids', [])),
                "emote_id": cmd.get('emote_id'),
                "timestamp": cmd.get('timestamp')
            }
            for i, cmd in enumerate(queue_list[:10])
        ]
    })

@app.route('/clear_queue')
def clear_queue():
    """Clear the queue (admin function)"""
    try:
        with queue_lock:
            command_queue.clear()
        return jsonify({
            "status": "success",
            "message": "Queue cleared successfully"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def run_flask():
    """Run Flask app"""
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"[Flask] Starting ZX BOSS API on port {port}")
    logger.info(f"[Flask] DEVELOPER: ZX BOSS 💥 ⁉️ ☠️")
    logger.info(f"[Flask] TELEGRAM: @ZXBOSS1 | CHANNEL: ZXOFFLCIAL11")
    logger.info(f"[Flask] Timing: Join=0.13s | Emotes=Simultaneous | Leave=0.05s | Gap=0.08s")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

async def main():
    """Main async function to run everything"""
    # Start Flask server in background thread
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
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
    logger.info("🔥 Starting ZX BOSS Free Fire Emote Bot...")
    logger.info("💥 DEVELOPER: ZX BOSS")
    logger.info("📱 TELEGRAM: @ZXBOSS1 | CHANNEL: ZXOFFLCIAL11")
    logger.info("⚡ Timing: Join=0.13s | Emotes=Simultaneous | Leave=0.05s | Gap=0.08s")

    asyncio.run(main())

