import asyncio
import ssl
import json
import random
from queue import Queue
import aiohttp
from xPARA import *
from xHeaders import *

# Global Variables
Chat_Leave = False
joining_team = False
login_url, ob, version = AuToUpDaTE()
command_queue = Queue()

class CLIENT:
    def __init__(self):
        self.whisper_writer = None
        self.online_writer = None
        self.uid = None
        self.room_uid = None
        self.inPuTMsG = None
        self.chat_id = None
        self.data = None
        self.data2 = None
        self.key = None
        self.iv = None
        self.AutHToKen = None
        self.OnLineiP = None
        self.OnLineporT = None
        self.ChaTiP = None
        self.ChaTporT = None
        self.LoGinDaTaUncRypTinG = None
        self.XX = None
        self.insquad = None
        self.sent_inv = None
        self.bot_ready = False
        self.current_squad_owner = None
        self.JWT = None

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
            return 'UnsoPorTed TypE ! >> ErrrroR (:():)'

    async def process_api_commands(self):
        """Process commands from API queue"""
        while True:
            try:
                if not command_queue.empty():
                    command = command_queue.get()
                    command_type = command.get('type')
                    
                    if command_type == 'join_and_emote':
                        team_code = command.get('team_code')
                        uids = command.get('uids', [])
                        emote_id = command.get('emote_id')
                        
                        # Join team using code
                        print(f"[API] Joining team with code: {team_code}")
                        join_packet = await GenJoinSquadsPacket(team_code, self.key, self.iv)
                        await self.SEndPacKeT(self.whisper_writer, self.online_writer, 'OnLine', join_packet)
                        
                        # Ultra-fast join wait (0.4 seconds)
                        await asyncio.sleep(0.4)
                        
                        # Prepare all emote packets simultaneously
                        emote_packets = []
                        for uid in uids:
                            if uid:
                                print(f"[API] Preparing emote {emote_id} for UID: {uid}")
                                emote_packet = await Emote_k(uid, emote_id, self.key, self.iv)
                                emote_packets.append(emote_packet)
                        
                        # Send ALL emote packets at once (no delays between)
                        for packet in emote_packets:
                            self.online_writer.write(packet)
                        await self.online_writer.drain()  # Single drain call
                        print(f"[API] Sent {len(emote_packets)} emotes simultaneously")
                        
                        # Minimal leave time
                        await asyncio.sleep(0.1)
                        
                        # Leave squad after emotes
                        leave_packet = await ExiT(None, self.key, self.iv)
                        await self.SEndPacKeT(self.whisper_writer, self.online_writer, 'OnLine', leave_packet)
                        print(f"[API] Command completed in ~0.5 seconds")
                        
            except Exception as e:
                print(f"[API] Error processing command: {e}")
            
            await asyncio.sleep(0.1)

    async def TcPOnLine(self, ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
        global Chat_Leave, joining_team
        while True:
            try:
                reader, writer = await asyncio.open_connection(ip, int(port))
                self.online_writer = writer
                bytes_payload = bytes.fromhex(AutHToKen)
                self.online_writer.write(bytes_payload)
                await self.online_writer.drain()
                
                print(f"[Online] Connected to {ip}:{port}")
                
                while True:
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
                                print(f"[API] Successfully joined squad, Owner UID: {OwNer_UiD}")
                            except Exception as e:
                                print(f"[API] Error joining squad chat: {e}")
                        
                        joining_team = False

                if self.whisper_writer is not None:
                    try:
                        self.whisper_writer.close()
                        await self.whisper_writer.wait_closed()
                    except Exception as e:
                        print(f"Error closing whisper_writer: {e}")
                    finally:
                        self.whisper_writer = None

                if self.online_writer is not None:
                    try:
                        self.online_writer.close()
                        await self.online_writer.wait_closed()
                    except Exception as e:
                        print(f"Error closing online_writer: {e}")
                    finally:
                        self.online_writer = None

                self.insquad = None

            except Exception as e:
                print(f"- Error With {ip}:{port} - {e}")
                self.online_writer = None
            await asyncio.sleep(reconnect_delay)

    async def TcPChaT(self, ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, reconnect_delay=0.5):
        global Chat_Leave, joining_team
        while True:
            try:
                reader, writer = await asyncio.open_connection(ip, int(port))
                self.whisper_writer = writer
                bytes_payload = bytes.fromhex(AutHToKen)
                self.whisper_writer.write(bytes_payload)
                await self.whisper_writer.drain()
                ready_event.set()
                
                print(f"[Chat] Connected to {ip}:{port}")
                
                if LoGinDaTaUncRypTinG.Clan_ID:
                    clan_id = LoGinDaTaUncRypTinG.Clan_ID
                    clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                    print('\n - Bot is in Clan!')
                    print(f' - Clan UID: {clan_id}')
                    pK = await AuthClan(clan_id, clan_compiled_data, key, iv)
                    if self.whisper_writer:
                        self.whisper_writer.write(pK)
                        await self.whisper_writer.drain()
                
                self.bot_ready = True
                print("[Bot] Ready to receive API commands!")
                
                while True:
                    self.data = await reader.read(9999)
                    data = self.data
                    if not data:
                        break

                if self.whisper_writer is not None:
                    try:
                        self.whisper_writer.close()
                        await self.whisper_writer.wait_closed()
                    except Exception as e:
                        print(f"Error closing whisper_writer: {e}")
                    finally:
                        self.whisper_writer = None

                if self.online_writer is not None:
                    try:
                        self.online_writer.close()
                        await self.online_writer.wait_closed()
                    except Exception as e:
                        print(f"Error closing online_writer: {e}")
                    finally:
                        self.online_writer = None

                self.insquad = None

            except Exception as e:
                print(f"Error {ip}:{port} - {e}")
                self.whisper_writer = None
            await asyncio.sleep(reconnect_delay)

    async def MaiiiinE(self):
        Uid, Pw = '4232977194','JOBAYAR_CODX-DJJWHJGQB'
        
        open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
        if not open_id or not access_token:
            print("Error - Invalid Account")
            return None

        PyL = await EncRypTMajoRLoGin(open_id, access_token)
        MajoRLoGinResPonsE = await MajorLogin(PyL)
        if not MajoRLoGinResPonsE:
            print("Target Account => Banned / Not Registered!")
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
            print("Error - Getting Ports From Login Data!")
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
        
        print(f" - Server Login URL => {login_url} | Server URL => {UrL}\n")
        print(f" - Game Status > Good | OB => {ob} | Version => {version}\n")
        print(f" - Bot Starting on Target: {AccountName}, UID: {TarGeT} | Region => {ReGioN}\n")
        print(f" - Bot Status > Good | Online!\n")
        print(f" - API Server running\n")
        print(f" - Ultra-Optimized Timing: Join=0.4s, Emotes=Simultaneous, Leave=0.1s\n")

        await asyncio.gather(task1, task2, task3)

# Global client instance
client = CLIENT()

async def StarTinG():
    while True:
        try:
            await asyncio.wait_for(client.MaiiiinE(), timeout=7 * 60 * 60)
        except asyncio.TimeoutError:
            print("Token Expired! Restarting...")
        except Exception as e:
            import traceback
            print(f"Error TCP - {e} => Restarting...")
            traceback.print_exc()

def start_bot():
    """Start the bot in a synchronous wrapper for threading"""
    asyncio.run(StarTinG())