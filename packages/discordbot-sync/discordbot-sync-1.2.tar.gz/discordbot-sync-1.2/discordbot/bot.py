'''
    discordbot is a program which provides an interface to the Discord API
    Copyright (C) 2021 Gabe Millikan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import asyncio
import time
import traceback
import psutil

import websockets, requests, urllib, json
import os, shutil, pathlib
file_root = pathlib.Path(__file__).parent / "_files"
file_root.mkdir(parents = True, exist_ok = True)

from discordbot import *

def default_logger(bot, severity, contents, no_message):
    line = ''
    if severity == log_severity.error:
        line = "[ERROR]: %s" % contents
    elif severity == log_severity.warning:
        line = "[WARNING]: %s" % contents
    elif severity == log_severity.important:
        line = "[IMPORTANT]: %s" % contents
    elif severity == log_severity.info:
        line = "[INFO]: %s" % contents
    elif severity == log_severity.debug:
        line = "[DEBUG]: %s" % contents
    else:
        line = "[UNKNOWN SEVERITY]: %s" % contents
    
    print(line)
    
class Bot:

    def get_active_pid():
        active_pid = None
        try:
            with open(file_root / "active", "r") as f:
                active_pid = int(f.read())
        except:
            # the file does not exist or is invalid
            pass
        return active_pid

    def __init__(self, token, sequence = 0, session_id = None, bot_identifier = "python/discordbot/v1.1", logger = default_logger):
        
        '''
            variables
        '''
        
        # log
        self.logger = logger
        self.logger_repeated_errors = 0
        
        # active
        self._is_active = False
        
        # bot
        self.token = token
        self._sequence = sequence
        self.session_id = session_id
        self.bot_identifier = bot_identifier
        self._die = False
        
        # gateway
        self._gateway_endpoint = None
        self._ws_conn = None
        self._ws_reconnect = False
        
        # command
        self._commands = {}
        self.command_prefix = "?"
        
        # event
        self._event_handlers = {}
        
        # rate limit
        self._rate_buckets = {}
        self._rate_bucket_lookup = {}
        
        # periodic tasks
        self._periodics = []
        self._stop_periodics = False
    
        '''
            activity
        '''
    
        # check if it's already running
        my_pid = os.getpid()
        active_pid = Bot.get_active_pid()
        if active_pid != None and psutil.pid_exists(active_pid):
            self.log("Bot not starting because another is already running (pid = %d)" % (active_pid))
            raise error.BotAlreadyRunning("The bot is already running elsewhere on the system. If this is not true, then please remove all files in the directory %s." % file_root)
        
        # write that i'm running
        self.log("Bot initialized.", severity = log_severity.info)
        self.log("Writing my pid (%d) to %s" % (my_pid, file_root / "active"))
        try:
            with open(file_root / "active", "w+") as f:
                f.write(str(my_pid))
        except BaseException as e:
            self.log_error(e)
            raise e
        self._is_active = True
        
        
        '''
            create default periodic tasks
        '''
        
        # continually check if another instance has been started
        async def check_pid(dt):
            active_pid = Bot.get_active_pid()
            if active_pid is None:
                self._is_active = False
                self.logout()
                raise error.DiscordError("Bot shutting down because %s was corrupted or deleted." % (file_root / "active"))
            elif active_pid != my_pid:
                self._is_active = False
                self.logout()
                raise error.BotAlreadyRunning("Another bot has been started (pid = %d) which has overrun my process (pid = %d). Logging out..." % (active_pid, my_pid))
        self.register_periodic(1, check_pid)
        
        # heartbeat
        self._heartbeat_interval = 45 # seconds
        self._time_since_heartbeat = 0
        async def heartbeat(dt):
            self._time_since_heartbeat += dt
            if self._ws_conn and self._time_since_heartbeat > self._heartbeat_interval:
                await self._send_payload(api.payload.OutgoingHeartbeat(self._sequence))
                self._time_since_heartbeat = 0
        self.register_periodic(0.1, heartbeat)
        
        # close connection on death
        async def check_death(dt):
            if self._die:
                self._stop_periodics = True
                try:
                    c = self._ws_conn
                    self._ws_conn = None
                    await c.close(1001) # not returning
                except:
                    pass
        self.register_periodic(0.1, check_death)
        
        '''
            events
        '''
        
        # command handler
        self.on_event(event.guild_message_sent, self._command_handler)
    
    def __del__(self):
        try:
            if self._is_active:
                os.remove(file_root / "active")
                self._is_active = False
        except:
            pass
    
    '''
        logging
    '''
    def log(self, txt, severity = log_severity.debug):
        try:
            self.logger(self, severity, txt, self.logger_repeated_errors)
        except BaseException as e:
            self.logger_repeated_errors += 1
            self.log_error(e)
            self.logger_repeated_errors = 0
    
    def log_error(self, err, severity = log_severity.error):
        self.log("%s\n%s" % (traceback.format_exc(), repr(err)), severity = severity)
    
    '''
        internal http utils
    '''
    def _wrap_http(self, method, *args, **kwargs):
        self.log("Sending HTTP %s request w/ args: %s and kwargs: %s" % (method.upper(), ", ".join(args), str(kwargs)))
    
        response = None
        try:
            response = {
                "get": requests.get,
                "post": requests.post,
                "put": requests.put,
                "delete": requests.delete,
            }[method.lower()](*args, **kwargs)
        except requests.RequestException as e:
            raise error.HTTPError(f"HTTP {method.upper()} request failed (w/ request error {e.__class__.__name__}) because: {str(e)}") from e
        
        sc = response.status_code
        if sc in api.status_code.http_success:
            data = {}
            if sc != api.status_code.no_content:
                try:
                    data = response.json()
                except:
                    raise error.UnexpectedResponse(f"Invalid JSON: {response.text}")
            return data, response
        elif sc in api.status_code.http_bad_request:
            raise error.HTTPBadRequest(f"Sent an invalid request, got response: {response.text}")
        elif sc in api.status_code.http_insufficient_permissions:
            raise error.HTTPBadRequest(f"Made request with insufficient permissions, got response: {response.text}")
        elif sc in api.status_code.http_try_later:
            t = 5
            if sc == api.status_code.too_many_requests:
                try:
                    t = response.json()['retry_after']
                except:
                    t = 10 # just assume 10
                    self.log(f"Got http rate limited, but response had no retry_after parameter. The response was: {response.text}", severity = log_severity.warning)
                    pass
            
            self.log("HTTP will wait %.1f seconds before retrying due to unexpected rate limit: %s" % (t, response.text))
            time.sleep(t)
            return self._wrap_http(method, *args, **kwargs)
        else:
            raise error.UnexpectedResponse("Got unknown HTTP status code: %d" % sc)
    
    def _rate_limited_http(self, method, url, *args, **kwargs):
        bucket_key = "%s / %s" % (method, url)
        
        if bucket_key in self._rate_bucket_lookup:
            bucket = self._rate_buckets[self._rate_bucket_lookup[bucket_key]]
            
            if bucket['remaining'] <= 0 and bucket['reset_at'] > time.time():
                t = bucket['reset_at'] - time.time()
                self.log("HTTP will wait %.1f seconds before retrying due to known bucket rate limit" % t)
                time.sleep(t)
            
            bucket['remaining'] -= 1
            
        data, response = self._wrap_http(method, url, *args, **kwargs)
        
        # attempt to parse the rate limit
        if "X-RateLimit-Bucket" in response.headers:
            bucket_id = str(response.headers["X-RateLimit-Bucket"])
            
            bucket = None
            if bucket_id in self._rate_buckets:
                bucket = self._rate_buckets[bucket_id]
            else:
                bucket = {
                    "reset_at": time.time() + 10,
                    "limit": 5,
                    "remaining": 4
                }
                self._rate_buckets[bucket_id] = bucket
            
            self._rate_bucket_lookup[bucket_key] = bucket_id
        
            if "Date" in response.headers and "X-RateLimit-Reset" in response.headers:
                discord_current_time = util.parse_date_header(response.headers["Date"])
                discord_time_of_reset = float(response.headers["X-RateLimit-Reset"])
                bucket["reset_at"] = time.time() + discord_time_of_reset - discord_current_time
            elif "X-RateLimit-Reset-After" in response.headers:
                bucket["reset_at"] = time.time() + float(response.headers["X-RateLimit-Reset-After"])
            
            if "X-RateLimit-Limit" in response.headers:
                bucket["limit"] = int(response.headers["X-RateLimit-Limit"])
            
            if "X-RateLimit-Remaining" in response.headers:
                bucket["remaining"] = int(response.headers["X-RateLimit-Remaining"])
        
        return data, response
    
    def _get_gateway(self):
        if self._gateway_endpoint is None:
            data, _ = self._wrap_http("get", "https://discord.com/api/v9/gateway")
            if not 'url' in data:
                raise error.UnexpectedResponse("response did not contain 'url' parameter: %s" % data)
            
            self._gateway_endpoint = data['url']
        
        return self._gateway_endpoint
    
    '''
        internal funcs
    '''
    async def _handle_event(self, evt, event_type, *data):
        if event_type in self._event_handlers:
            for f in self._event_handlers[event_type]:
                try:
                    await util.call_func(f, evt.data, *data)
                except BaseException as e:
                    raise error.CallbackError("Event callback '%s' for '%s' failed." % (repr(f), event_type)) from e
    
    async def _run_periodics(self):
        self.log("Periodic tasks are now running.")
        while not self._stop_periodics:
            for d in self._periodics:
                [call_rate, time_last_called, f] = d
                
                dt = time.time() - time_last_called
                if dt < call_rate:
                    continue
                
                try:
                    await util.call_func(f, dt)
                except BaseException as e:
                    p_err = error.CallbackError("Periodic function '%s' errored." % repr(f))
                    p_err.__cause__ = e
                    self.log_error(p_err)
                
                d[1] = time.time()
            try:
                await asyncio.sleep(0.01)
            except BaseException as e:
                self.log(str(e))
        self.log("Periodic tasks have stopped.")
    
    async def _send_payload(self, pl):
        assert isinstance(pl, api.payload.OutgoingPayload), "payload must be discordbot.api.payload.OutgoingPayload"
        await self._ws_conn.send(pl.dumps())
        
    async def _wait_for_valid_payload(self):
        while True:
            try:
                return api.payload.Payload(await self._ws_conn.recv())
            except error.ReceivedInvalidPayload as e:
                self.log_error(e)
    
    async def _wait_for_payload(self, opcode, wait_for_correct_opcode = False):
        while True:
            pl = await self._wait_for_valid_payload()
            if pl.opcode == opcode:
                return pl
            else:
                s = "Waiting for payload w/ opcode %d but got one with opcode %d" % (opcode, pl.opcode)
                self.log(s)
                if not wait_for_correct_opcode:
                    raise error.DiscordError(s)
    
    async def _wait_for_valid_event(self, wait_for_event = False):
        while True:
            try:
                return api.payload.Event(await self._wait_for_payload(api.opcode.event, wait_for_correct_opcode = wait_for_event))
            except error.InvalidEventPayload as e:
                self.log_error(e)
    
    async def _wait_for_event(self, event_name, wait_for_event = False, wait_for_correct_event = True):
        while True:
            evt = await self._wait_for_valid_event(wait_for_event = wait_for_event)
            if evt.name == event_name:
                return evt
            else:
                s = "Waiting for event w/ name %s but got one with name %s" % (event_name, evt.name)
                self.log(s)
                if not wait_for_correct_event:
                    raise error.DiscordError(s)
    
    async def _on_payload_received(self, pl):
        if pl.opcode == api.opcode.event:
            evt = api.payload.Event(pl)
            self._sequence = max(self._sequence, evt.sequence)
            if evt.name == 'MESSAGE_CREATE':
                evt = api.payload.MessageCreateEvent(evt)
                await self._handle_event(evt, event.guild_message_sent, evt.message)
            elif evt.name == "MESSAGE_UPDATE":
                evt = api.payload.MessageEditEvent(evt)
                if evt.after == None:
                    evt.after = self.get_message(evt.data["channel_id"], evt.data["id"])
                await self._handle_event(evt, event.guild_message_edited, evt.before, evt.after)
            elif evt.name == "MESSAGE_DELETE":
                evt = api.payload.MessageDeleteEvent(evt)
                await self._handle_event(evt, event.guild_message_deleted, evt.message)
            elif evt.name == "GUILD_CREATE":
                evt = api.payload.GuildCreateEvent(evt)
                await self._handle_event(evt, event.guild_created, evt.guild)
            elif evt.name == "MESSAGE_DELETE_BULK":
                evt = api.payload.MessageBulkDeleteEvent(evt)
                await self._handle_event(evt, event.guild_message_bulk_delete, evt.messages, evt.channel, evt.guild)
            elif evt.name == "RESUMED":
                pass
            else:
                self.log("Unknown event received: %s" % evt, severity = log_severity.warning)
        elif pl.opcode == api.opcode.heartbeat_ack:
            pass
        elif pl.opcode == api.opcode.reconnect or pl.opcode == api.opcode.session_invalidated:
            self._ws_reconnect = True
            if pl.opcode == api.opcode.session_invalidated:
                self.session_id = None
        else:
            self.log("Unknown payload received: %s" % pl, severity = log_severity.warning)
    
    async def _open_websocket(self):
        # get gateway endpoint
        wss_endpoint = self._get_gateway()
        
        # connect to it
        self._ws_conn = await websockets.connect(wss_endpoint)
    
    async def _connect(self):
        # open ws
        self.log("Opening websocket connection...")
        try:
            await self._open_websocket()
        except BaseException as e:
            raise error.GatewayError("Failed to open websocket connection.") from e
        
        # receive hello
        self.log("Waiting for hello payload...")
        hello = api.payload.Hello(await self._wait_for_payload(api.opcode.hello))
        self._heartbeat_interval = hello.heartbeat_interval
        self.log("Discord gateway says hello! Heartbeat interval is %.1f seconds." % self._heartbeat_interval)
        
        # send initial heartbeat
        self.log("Replying with initial heartbeat...")
        await self._send_payload(api.payload.OutgoingHeartbeat(self._sequence))
        
        # wait for ACK
        self.log("Waiting for initial ACK...")
        await self._wait_for_payload(api.opcode.heartbeat_ack)
        
        # connected!
        self.log("Websocket connection is open and alive!")
        return True
    
    async def _ws_init_identify(self):
        # identify
        self.log("Identifying...")
        await self._send_payload(api.payload.OutgoingIdentify(
            self.token,
            self.intents,
            self.bot_identifier
        ))
        
        # wait for ready event
        self.log("Waiting for READY event...")
        ready = api.payload.ReadyEvent(await self._wait_for_event('READY'))
        self.log("Logged in as %s - Got session id: %s" % (ready.user, ready.session_id))
        self.user = ready.user
        self.session_id = ready.session_id
        self._sequence = 0
        
        return ready
    
    async def _ws_init_resume(self):
        self.log("Resuming from sequence %d using session id %s..." % (self._sequence, self.session_id))
        await self._send_payload(api.payload.Resume(
            self.token,
            self.session_id,
            self._sequence
        ))
        self.log("Now resuming.")
        return True
    
    async def _attempt_full_connect(self):
        self.log("Attempting full gateway connection (sequence = %d, sessionid = %s)." % (self._sequence, self.session_id))
        
        # close the previous websocket (if there is one)
        try:
            if self._ws_conn != None:
                await self._ws_conn.close(1000)
        except:
            # it was already closed
            pass
        self._ws_conn = None
        
        # open a new connection
        try:
            await self._connect()
        except BaseException as e:
            raise error.GatewayError("Failed to connect to gateway.") from e
        
        # identify or resume
        if self.session_id == None:
            ready = None
            try:
                ready = await self._ws_init_identify()
            except BaseException as e:
                raise error.GatewayError("Failed to identify, perhaps invalid bot token?") from e
            
            self.log("Running ready event after identify success.")
            await self._handle_event(ready, event.ready)
        else:
            try:
                await self._ws_init_resume()
            except BaseException as e:
                p_err = error.GatewayError("Failed to resume connection after disconnect, perhaps the sessionid was invalidated?")
                p_err.__cause__ = e
                self.log_error(p_err)
                
                # probably invalid session id, try again without the resume
                self.log("Resume failed - retrying without resuming (some events may be dropped).")
                self.session_id = None
                self._sequence = 0
                return await self._attempt_full_connect()
        
        self.log("Full gateway connection successful! Now ready to receive normal payloads.")
        return True
        
    async def _ws_payload_loop(self):
        # wait for a payload
        pl = await self._wait_for_valid_payload()
        
        # log it
        if pl.opcode == api.opcode.event:
            self.log("Received event payload: %s" % pl.raw['t'])
        else:
            self.log("Received payload: [%d] %s" % (pl.opcode, api.opcode.get_name(pl.opcode)))
        
        # process it
        try:
            await self._on_payload_received(pl)
        except error.DiscordError as e:
            self.log_error(e)
    
    async def _run(self):
        self.log("Bot is running...")
        self._periodic_task = asyncio.create_task(self._run_periodics())
        
        while not self._die:
            self.log("Bot has not died, will connect and begin looping over payloads.")
            try:
                self._ws_reconnect = False
                await self._attempt_full_connect()
                while True:
                    await self._ws_payload_loop()
                    if self._ws_reconnect or self._die:
                        break
            except BaseException as e:
                if util.error_caused_by(e, websockets.ConnectionClosedError):
                    if self._ws_conn:
                        if self._ws_conn.close_code == 4004:
                            p_err = error.DiscordError("Invalid bot token.")
                            p_err.__cause__ = e
                            self.log_error(p_err)
                            return False
                        elif self._ws_conn.close_code == 4009:
                            self.session_id = None
                        self.log("Bot will reconnect due to websocket closing with code %d." % self._ws_conn.close_code)
                    self._ws_reconnect = True
                
                if self._ws_reconnect:
                    continue
                
                if util.error_caused_by(e, (KeyboardInterrupt, asyncio.CancelledError)):
                    self._die = True
                    self.log("Bot shutting down due to KeyboardInterrupt or asyncio.CancelledError.", severity = log_severity.info)
                    return True
                
                self.log_error(e)
                return False
                
        self.log("Bot died due to normal operations.")
        return True
    
    def _command_handler(self, raw, message):
        if not message.content.startswith(self.command_prefix):
            return
        
        if not "member" in message.raw:
            return
        if not "roles" in message.raw["member"]:
            return
        roles = [str(x) for x in message.raw["member"]["roles"]]
        
        parts = message.content.replace("\u200b", "").split()
        sent_cmd = parts[0][len(self.command_prefix):]
        sent_args = parts[1:]
        
        for cmd in self._commands:
            if not sent_cmd in cmd.split("_,_"):
                continue
            
            cmd_info = self._commands[cmd]
            if cmd_info['required_role'] != None and not cmd_info['required_role'] in roles:
                return
            
            # make sure that the correct arguments are present
            use_args = []
            for arg_info in cmd_info['args']:
            
                if len(sent_args) <= 0:
                    if 'default' in arg_info:
                        use_args.append(arg_info['default'])
                    else:
                        return # invalid
                else:
                    arg = sent_args.pop(0)
                    
                    if arg_info['type'] == "int":
                        try:    
                            arg = int(arg)
                        except:
                            return
                        if 'min' in arg_info and arg < arg_info['min']:
                            return
                        if 'max' in arg_info and arg > arg_info['max']:
                            return
                    elif arg_info['type'] == "user":
                        # try to get their ID
                        arg = ''.join([c for c in arg if '0' <= c <= '9']) # i love python
                        try:
                            n = int(arg)
                            assert n > 1_000_000
                        except:
                            return
                        
                        # convert to a user
                        user = None
                        if "mentions" in message.raw:
                            for m in message.raw["mentions"]:
                                if str(m["id"]) == arg:
                                    user = api.structure.User(m)
                                    break
                        if user is None:
                            user = api.structure.User({"id": arg})
                        
                        arg = user
                    
                    use_args.append(arg)
            
            cmd_info['handler'](message, *use_args)
            break
    
    '''
        user-exposed apis
    '''
    def on_event(self, evt, callback):
        assert issubclass(evt, event.Base), "event must be a discordbot.event"
        if not evt in self._event_handlers:
            self._event_handlers[evt] = []
        self._event_handlers[evt].append(callback)
    
    def remove_callback(self, evt, callback):
        assert evt in self._event_handlers and callback in self._event_handlers[evt], "event callback is not registered, you must Bot.on_event() it first"
        self._event_handlers[evt].remove(callback)
        if len(self._event_handlers[evt]) == 0:
            del self._event_handlers[evt]
    
    def register_periodic(self, dt, callback):
        self._periodics.append([dt, time.time(), callback])
    
    def add_role(self, guild, user, role):
        if isinstance(guild, api.structure.Guild):
            guild = guild.id
        if isinstance(user, api.structure.User):
            user = user.id
            
        data, _ = self._rate_limited_http(
            "put",
            "https://discord.com/api/v9/guilds/%s/members/%s/roles/%s" % (guild, user, role),
            headers = {
                "Authorization": "Bot %s" % self.token,
                "Content-Type": "application/json"
            }
        )
        return data
    
    def remove_role(self, guild, user, role):
        if isinstance(guild, api.structure.Guild):
            guild = guild.id
        if isinstance(user, api.structure.User):
            user = user.id
            
        data, _ = self._rate_limited_http(
            "delete",
            "https://discord.com/api/v9/guilds/%s/members/%s/roles/%s" % (guild, user, role),
            headers = {
                "Authorization": "Bot %s" % self.token,
                "Content-Type": "application/json"
            }
        )
        return data
    
    def send_message(self, channel, content = '', embeds = [], reply_to = None, force_reply = False, reply_ping = None, allowed_mentions = None):
        if isinstance(channel, api.structure.Channel):
            channel = channel.id
        
        info = {
            "content": content,
            "embeds": embeds,
        }
        
        if reply_to != None:
            if isinstance(reply_to, api.structure.Message):
                reply_to = reply_to.id
            info["message_reference"] = {
                "message_id": reply_to,
                "fail_if_not_exists": force_reply
            }
        
        if reply_ping != None:
            if allowed_mentions == None:
                allowed_mentions = {"parse": ["roles", "users", "everyone"]}
            if "replied_user" in allowed_mentions and allowed_mentions["replied_user"] != reply_ping:
                self.log("In send_message, tried to set allowed_mentions[\"replied_user\"] AND reply_ping parameter. Using reply_ping instead.", severity = log_severity.warning)
            allowed_mentions["replied_user"] = reply_ping
        info["allowed_mentions"] = allowed_mentions
        
        try:
            data, _ = self._rate_limited_http(
                "post",
                "https://discord.com/api/v9/channels/%s/messages" % channel,
                json.dumps(info),
                headers = {
                    "Authorization": "Bot %s" % self.token,
                    "Content-Type": "application/json"
                }
            )
            
            try:
                return api.structure.Message(data)
            except error.InvalidAPIObject as e:
                raise error.UnexpectedResponse("Response was not a valid Message object: %s" % e)
        except error.DiscordError as e:
            raise error.MessageSendFailure(str(e))
    
    def get_messages(self, channel, n):
        if isinstance(channel, api.structure.Channel):
            channel = channel.id
        result, response = self._rate_limited_http(
            "get",
            "https://discord.com/api/v9/channels/%s/messages" % channel,
            params = {
                "limit": n
            },
            headers = {
                "Authorization": "Bot %s" % self.token,
                "Content-Type": "application/json"
            }
        )
        if not isinstance(result, list):
            raise error.UnexpectedResponse("Did not return list, actually got:", result)
        
        for i in range(len(result)):
            try:
                result[i] = api.structure.Message(result[i])
            except error.InvalidAPIObject as e:
                raise error.UnexpectedResponse("Response had invalid message at index[%d]: %s" % (i, e))
        
        return result
    
    def get_message(self, channel, message_id):
        if isinstance(channel, api.structure.Channel):
            channel = channel.id
        if isinstance(message_id, api.structure.Message):
            message_id = message_id.id
        result, response = self._rate_limited_http(
            "get",
            "https://discord.com/api/v9/channels/%s/messages/%s" % (channel, message_id),
            headers = {
                "Authorization": "Bot %s" % self.token,
                "Content-Type": "application/json"
            }
        )
        
        try:
            result = api.structure.Message(result)
        except error.InvalidAPIObject as e:
            raise error.UnexpectedResponse("Response had invalid message w/ error: %s" % (e))
        
        return result
    
    def purge(self, channel, n):
        n = min(max(n, 1), 100)
        if isinstance(channel, api.structure.Channel):
            channel = channel.id
        
        messages = self.get_messages(channel, n)
        ids = [m.id for m in messages]
        
        result, response = self._rate_limited_http(
            "post",
            "https://discord.com/api/v9/channels/%s/messages/bulk-delete" % channel,
            json.dumps({
                "messages": ids,
            }),
            headers = {
                "Authorization": "Bot %s" % self.token,
                "Content-Type": "application/json"
            }
        )
        
        return len(ids)
    
    def kick(self, guild, member, reason = None):
        if isinstance(guild, api.structure.Guild):
            guild = guild.id
        if isinstance(member, api.structure.User):
            member = member.id
        
        headers = {
            "Authorization": "Bot %s" % self.token,
            "Content-Type": "application/json"
        }
        if reason != None:
            headers["X-Audit-Log-Reason"] = str(reason)
        
        
        data, _ = self._rate_limited_http(
            "delete",
            "https://discord.com/api/v9/guilds/%s/members/%s" % (guild, member),
            headers = headers
        )
        return data
        
    def ban(self, guild, member, reason = None, delete_message_days = 0):
        if isinstance(guild, api.structure.Guild):
            guild = guild.id
        if isinstance(member, api.structure.User):
            member = member.id
        
        headers = {
            "Authorization": "Bot %s" % self.token,
            "Content-Type": "application/json"
        }
        if reason != None:
            headers["X-Audit-Log-Reason"] = str(reason)
        
        data, _ = self._rate_limited_http(
            "put",
            "https://discord.com/api/v9/guilds/%s/bans/%s" % (guild, member),
            json.dumps({
                "delete_message_days": delete_message_days
            }),
            headers = headers
        )
        return data
    
    def stop(self):
        self._die = True
    logout = stop
    kill = stop
    
    def reconnect(self):
        self._ws_reconnect = True
    
    def register_command(self, cmd, description, handler, required_role = None, args = []):
        assert isinstance(cmd, (list, str)), "cmd may only be a string or list of strings"
        if isinstance(cmd, list):
            assert all(map(lambda x: isinstance(x, str), cmd)), "list of commands must only contain strings"
        
        cmd_key = cmd if isinstance(cmd, str) else "_,_".join(cmd)
        if cmd_key in self._commands:
            self.log("called register_command with command name that is already registered (\"%s\"). Overwriting." % cmd_key, severity = log_severity.warning)
        self._commands[cmd_key] = {
            "description": str(description),
            "handler": handler,
            "required_role": str(required_role) if required_role != None else None,
            "args": args
        }
    
    def register_default_commands(self):
        # just reply "pong"
        def cmd_ping(message):
            self.send_message(message.channel, "Pong!", reply_to = message, reply_ping = False)
        self.register_command("ping", "The bot will reply 'Pong!'", cmd_ping)
        
        # show commands list
        def cmd_cmds(message):
            self.send_message(message.channel, embeds = [
                {
                    "fields": [
                        {
                            "name": "%s%s %s" % (
                                self.command_prefix.replace("`", "\\`"),
                                ("{" + ', '.join(cmd.split("_,_")) + "}") if cmd.count("_,_") >= 1 else cmd,
                                ' '.join(["[%s]" % a['name'] for a in info['args']])
                            ),
                            "value": "%s\n%s" % (
                                "@everyone" if info["required_role"] is None else util.mention_role(info["required_role"]),
                                info["description"]
                            )
                        } for (cmd, info) in self._commands.items() 
                    ]
                }
            ], allowed_mentions = {
                "parse": []
            }, reply_to = message, reply_ping = False)
        self.register_command("cmds", "Shows a list of the bot's commands", cmd_cmds)
    
    def run(self, intents = [intent.guild_messages]):
        self.intents = util.get_flags(*intents)
        success = False
        try:
            success = asyncio.run(self._run())
        except KeyboardInterrupt as e:
            success = True
        return success