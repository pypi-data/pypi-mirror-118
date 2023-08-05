from __future__ import annotations
from .websocket import DefectioClientWebSocketResponse

import sys

from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Union, Coroutine
from . import __version__
import ulid
import logging
import aiohttp

if TYPE_CHECKING:
    import aiohttp
    from .types.payloads import (
        Account,
        ApiInfo,
        DMChannel,
        Login,
        MutualFriends,
        Profile,
        Relationship,
        RelationshipStatus,
        Session,
        Channel,
        User,
        ChannelInvite,
        EditChannel,
        FetchMessage,
        Group,
        JoinCall,
        Message,
        MessagePoll,
        SearchMessage,
        Server,
        Bans,
        Bot,
        CreateRole,
        Invite,
        JoinInvite,
        Member,
        PublicBot,
        ServerMembers,
        Settings,
        Unreads,
    )

    Response = Coroutine[Any, Any, T]

logger = logging.getLogger("defectio")


class HttpClient:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        api_url: str,
    ):
        self._session = session if session is not None else aiohttp.ClientSession()
        self.token: Optional[str] = None
        # self.api_info = api_info
        self.api_url = api_url
        user_agent = "Defectio (https://github.com/Darkflame72/defectio {0}) Python/{1[0]}.{1[1]} aiohttp/{2}"
        self.user_agent: str = user_agent.format(
            __version__, sys.version_info, aiohttp.__version__
        )
        self.is_bot = True

    def recreate(self) -> None:
        if self._session.closed:
            self._session = aiohttp.ClientSession(
                connector=self.connector,
                ws_response_class=DefectioClientWebSocketResponse,
            )

    async def ws_connect(self, url: str, *, compress: int = 0) -> Any:
        kwargs = {
            "proxy_auth": self.proxy_auth,
            "proxy": self.proxy,
            "max_msg_size": 0,
            "timeout": 30.0,
            "autoclose": False,
            "headers": {
                "User-Agent": self.user_agent,
            },
            "compress": compress,
        }

        return await self._session.ws_connect(url, **kwargs)

    async def request(
        self, method: str, path: str, *, auth_needed=True, **kwargs: Any
    ) -> Any:
        url = f"{self.api_url}/{path}"
        headers = kwargs.get("headers", {})
        headers["User-Agent"] = self.user_agent
        if auth_needed:
            if self.is_bot and self.token is not None:
                headers["x-bot-token"] = self.token
            else:
                raise Exception("Not authenticated")
        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            # kwargs["data"] = utils._to_json(kwargs.pop("json"))
        kwargs["headers"] = headers

        response: Optional[aiohttp.ClientResponse] = None
        data: Optional[Union[Dict[str, Any], str]] = None

        # Generate nonce for post messages
        if method == "POST":
            kwargs["json"] = kwargs.get("json", {})
            kwargs["json"]["nonce"] = ulid.new().str

        async with self._session.request(method, url, **kwargs) as response:
            data = await response.json()
            if 300 > response.status >= 200:
                logger.debug("%s %s has received %s", method, url, data)
                return data

    async def close(self) -> None:
        if self._session:
            await self._session.close()

    async def node_info(self) -> Response[ApiInfo]:
        path = ""
        return await self.request("GET", path, auth_needed=False)

    ################
    ## Onboarding ##
    ################

    async def check_onboarding(self):
        path = "onboard/hello"
        return await self.request("GET", path)

    async def complete_onboarding(self, username: str):
        path = "onboard/complete"
        return await self.request("GET", path, json={"username": username})

    ##########
    ## Auth ##
    ##########

    async def create_account(self, email: str, password: str, **kwargs):
        path = "auth/create"
        kwargs["email"] = email
        kwargs["password"] = password
        return await self.request("POST", path, json=kwargs, auth_needed=False)

    async def resend_verification(self, email: str, **kwargs) -> None:
        path = "auth/resend"
        kwargs["email"] = email
        return await self.request("POST", path, json=kwargs, auth_needed=False)

    async def login(self, email: str, password: str, **kwargs) -> Response[Login]:
        path = "auth/login"
        kwargs["email"] = email
        kwargs["password"] = password
        return await self.request(
            "POST", path, json={"email": email, "password": password}, auth_needed=False
        )

    async def send_password_reset(self, email: str, **kwargs):
        path = "auth/send_reset"
        kwargs["email"] = email
        return await self.request("POST", path, json=kwargs, auth_needed=False)

    async def confirm_password_reset(self, password: str, token: str):
        path = "/auth/reset"
        return await self.request(
            "POST", path, json={"password": password, "token": token}, auth_needed=False
        )

    async def get_account(self) -> Response[Account]:
        path = "auth/user"
        return await self.request("GET", path)

    async def check_auth(self):
        path = "auth/check"
        return await self.request("GET", path)

    async def change_password(self, old_password: str, new_password: str):
        path = "auth/change/password"
        return await self.request(
            "POST",
            path,
            json={"password": old_password, "new_password": new_password},
        )

    async def change_email(self, password: str, email: str):
        path = "auth/change/email"
        return await self.request("POST", path, json={"email": email})

    async def delete_session(self, session_id: str):
        path = f"auth/sessions/{session_id}"
        return await self.request("POST", path)

    async def get_sessions(self) -> Response[List[Session]]:
        path = "auth/sessions"
        return await self.request("GET", path)

    async def logout(self):
        path = "auth/logout"
        return await self.request("POST", path)

    ######################
    ## User Information ##
    ######################

    ## Self

    async def edit_self(self, **kwargs):
        path = "users/@me"
        return await self.request("PATCH", path, json=kwargs)

    async def change_username(self, username: str, password: str):
        path = "users/@me/username"
        return await self.request(
            "PATCH", path, json={"username": username, "password": password}
        )

    ## Users

    async def get_user(self, user_id: str) -> Response[User]:
        path = f"users/{user_id}"
        return await self.request("GET", path)

    async def get_user_profile(self, user_id: str) -> Response[Profile]:
        path = f"users/{user_id}/profile"
        return await self.request("GET", path)

    async def get_user_default_avatar(self, user_id: str):
        path = f"users/{user_id}/default_avatar"
        return await self.request("GET", path)

    async def get_mutual_friends(self, user_id: str) -> Response[MutualFriends]:
        path = f"users/{user_id}/mutual_friends"
        return await self.request("GET", path)

    ######################
    ## Direct Messaging ##
    ######################

    async def get_dms(self) -> Response[List[DMChannel]]:
        path = "users/dms"
        return await self.request("GET", path)

    async def open_dm(self, user_id: str) -> Response[DMChannel]:
        path = f"users/{user_id}/dm"
        return await self.request("POST", path)

    ###################
    ## Relationships ##
    ###################

    async def get_relationships(self) -> Response[List[Relationship]]:
        path = "users/relationships"
        return await self.request("GET", path)

    async def get_relationship(self, user_id: str) -> Response[Relationship]:
        path = f"users/{user_id}/relationships"
        return await self.request("GET", path)

    async def friend_request(self, user_id: str) -> Response[RelationshipStatus]:
        path = f"users/{user_id}/friend"
        return await self.request("PUT", path)

    async def remove_friend(self, user_id: str) -> Response[RelationshipStatus]:
        path = f"users/{user_id}/friend"
        return await self.request("DELETE", path)

    async def block_user(self, user_id: str) -> Response[RelationshipStatus]:
        path = f"users/{user_id}/block"
        return await self.request("PUT", path)

    async def unblock_user(self, user_id: str) -> Response[RelationshipStatus]:
        path = f"users/{user_id}/block"
        return await self.request("DELETE", path)

    #########################
    ## Channel Information ##
    #########################

    async def get_channel(self, channel_id: str) -> Response[Channel]:
        path = f"channels/{channel_id}"
        return await self.request("GET", path)

    async def edit_channel(self, channel_id: str, **kwargs) -> Response[EditChannel]:
        path = f"channels/{channel_id}"
        return await self.request("PATCH", path, json=kwargs)

    async def close_channel(self, channel_id: str):
        path = f"channels/{channel_id}"
        return await self.request("DELETE", path)

    #####################
    ## Channel Invites ##
    #####################

    async def create_channel_invite(self, channel_id: str) -> Response[ChannelInvite]:
        path = f"channels/{channel_id}/invites"
        return await self.request("POST", path)

    #########################
    ## Channel Permissions ##
    #########################

    async def set_channel_role_permissions(
        self, channel_id: str, role_id: str, permissions: int
    ):
        path = f"channels/{channel_id}/permissions/{role_id}"
        return await self.request("PUT", path, json={"permissions": permissions})

    async def set_channel_default_role_permissions(
        self, channel_id: str, permissions: int
    ):
        path = f"channels/{channel_id}/permissions/default"
        return await self.request("PUT", path, json={"permissions": permissions})

    ###############
    ## Messaging ##
    ###############

    async def send_message(
        self,
        channel_id: str,
        content: str,
        *,
        attachments: Optional[List[Any]] = None,
        replies: Optional[Any] = None,
    ) -> Response[Message]:
        path = f"channels/{channel_id}/messages"
        json = {"content": content}
        if attachments:
            json["attachments"] = attachments
        if replies:
            json["replies"] = replies
        return await self.request("POST", path, json=json)

    async def get_messages(
        self,
        channel_id: str,
        *,
        limit: int = 100,
        before: Optional[str] = None,
        after: Optional[str] = None,
        sort: Literal["Latest", "Oldest"] = "Latest",
        nearby: Optional[List[str]] = None,
        include_users: bool = True,
    ) -> Response[List[FetchMessage]]:
        path = f"channels/{channel_id}/messages"
        json = {"sort": sort}
        if limit:
            json["limit"] = limit
        if before:
            json["before"] = before
        if after:
            json["after"] = after
        if nearby:
            json["nearby"] = nearby
        if not include_users:
            json["include_users"] = include_users
        return await self.request("GET", path, json=json)

    async def get_message(self, channel_id: str, message_id: str) -> Response[Message]:
        path = f"channels/{channel_id}/messages/{message_id}"
        return await self.request("GET", path)

    async def edit_message(
        self,
        channel_id: str,
        message_id: str,
        content: str,
    ):
        path = f"channels/{channel_id}/messages/{message_id}"
        return await self.request("PATCH", path, json={"content": content})

    async def delete_message(self, channel_id: str, message_id: str):
        path = f"channels/{channel_id}/messages/{message_id}"
        return await self.request("DELETE", path)

    async def poll_message_changes(
        self, channel_id: str, message_ids: List[str]
    ) -> Response[MessagePoll]:
        path = f"channels/{channel_id}/messages/stale"
        return await self.request("GET", path, json=message_ids)

    async def search_message(
        self,
        channel_id: str,
        query: str,
        *,
        limit: int = 100,
        before: Optional[str] = None,
        after: Optional[str] = None,
        sort: Literal["Latest", "Oldest", "Relevant"] = "Latest",
        include_users: bool = True,
    ) -> Response[SearchMessage]:
        path = f"channels/{channel_id}/messages/search"
        json = {"query": query, "sort": sort, "include_users": include_users}
        if limit:
            json["limit"] = limit
        if before:
            json["before"] = before
        if after:
            json["after"] = after
        return await self.request("GET", path, json=json)

    async def acknoledge_message(self, channel_id: str, message_id: str):
        path = f"channels/{channel_id}/ack/{message_id}"
        return await self.request("PUT", path)

    ############
    ## Groups ##
    ############

    async def create_group(
        self,
        name: str,
        *,
        description: Optional[str] = None,
        users: Optional[List[str]] = None,
    ) -> Response[Group]:
        path = "channels/create"
        json = {"name": name}
        if description:
            json["description"] = description
        if users:
            json["users"] = users
        return await self.request("POST", path, json=json)

    async def get_group_members(self, group_id: str) -> Response[List[User]]:
        path = f"channels/{group_id}/members"
        return await self.request("GET", path)

    async def add_group_member(self, group_id: str, user_id: str):
        path = f"channels/{group_id}/recipients/{user_id}"
        return await self.request("PUT", path)

    async def remove_group_member(self, group_id: str, user_id: str):
        path = f"channels/{group_id}/members/recipients/{user_id}"
        return await self.request("DELETE", path)

    async def join_call(self, channel_id: str) -> Response[JoinCall]:
        path = f"channels/{channel_id}/join_call"
        return await self.request("POST", path)

    ########################
    ## Server Information ##
    ########################

    async def get_server(self, server_id: str) -> Response[Server]:
        path = f"servers/{server_id}"
        return await self.request("GET", path)

    async def edit_server(
        self,
        server_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        icon: Optional[str] = None,
        banner: Optional[str] = None,
        categories: Optional[List[Any]] = None,
        system_messages: Optional[Any] = None,
        remove: Optional[Literal["Banner", "Description", "Icon"]] = None,
    ):
        path = f"servers/{server_id}"
        json = {}
        if name:
            json["name"] = name
        if description:
            json["description"] = description
        if icon:
            json["icon"] = icon
        if banner:
            json["banner"] = banner
        if categories:
            json["categories"] = categories
        if system_messages:
            json["system_messages"] = system_messages
        if remove:
            json["remove"] = remove
        return await self.request("PATCH", path, json=json)

    async def remove_server(self, server_id: str):
        path = f"servers/{server_id}"
        return await self.request("DELETE", path)

    async def create_server(
        self, name: str, *, description: Optional[str] = None
    ) -> Response[Server]:
        path = "servers/create"
        json = {"name": name}
        if description:
            json["description"] = description
        return await self.request("POST", path, json=json)

    async def create_channel(
        self,
        server_id: str,
        name: str,
        *,
        type: Literal["Text", "Voice"] = "Text",
        description: Optional[str] = None,
    ) -> Response[Channel]:
        path = f"servers/{server_id}/channels"
        json = {"name": name, "type": type}
        if description:
            json["description"] = description
        return await self.request("POST", path, json=json)

    async def get_invite(self, server_id: str):
        path = f"invites/{server_id}/invites"
        return await self.request("GET", path)

    async def mark_channels_read(self, server_id: str):
        path = f"channels/{server_id}/ack"
        return await self.request("POST", path)

    ####################
    ## Server Members ##
    ####################

    async def get_member(self, server_id: str, member_id: str) -> Response[Member]:
        path = f"servers/{server_id}/members/{member_id}"
        return await self.request("GET", path)

    async def edit_member(
        self,
        server_id: str,
        member_id: str,
        *,
        nickname: Optional[List[str]] = None,
        roles: Optional[List[str]] = None,
        avatar: Optional[str] = None,
        remove: Optional[Literal["Avatar", "Nickname"]] = None,
    ):
        path = f"servers/{server_id}/members/{member_id}"
        json = {}
        if roles:
            json["roles"] = roles
        if nickname:
            json["nick"] = nickname
        if avatar:
            json["avatar"] = avatar
        if remove:
            json["remove"] = remove
        return await self.request("PATCH", path, json=json)

    async def kick_member(self, server_id: str, member_id: str):
        path = f"servers/{server_id}/members/{member_id}"
        return await self.request("DELETE", path)

    async def get_members(self, server_id: str) -> Response[ServerMembers]:
        path = f"servers/{server_id}/members"
        return await self.request("GET", path)

    async def ban_member(
        self, server_id: str, member_id: str, reason: Optional[str] = None
    ):
        path = f"servers/{server_id}/ban/{member_id}"
        json = {"reason": reason}
        return await self.request("PUT", path, json=json)

    async def unban_member(self, server_id: str, member_id: str):
        path = f"servers/{server_id}/ban/{member_id}"
        return await self.request("DELETE", path)

    async def get_bans(self, server_id: str) -> Response[Bans]:
        path = f"servers/{server_id}/bans"
        return await self.request("GET", path)

    ########################
    ## Server Permissions ##
    ########################

    async def set_server_role_permissions(
        self, server_id: str, role_id: str, *, permissions: int
    ):
        path = f"servers/{server_id}/permissions/{role_id}"
        return await self.request("PUT", path, json={"permissions": 0})

    async def set_server_default_role_permissions(
        self, server_id: str, permissions: int
    ):
        path = f"servers/{server_id}/permissions/default_role"
        return await self.request("PUT", path, json={"permissions": permissions})

    async def create_role(self, server_id: str, *, name: str) -> Response[CreateRole]:
        path = f"servers/{server_id}/roles"
        json = {"name": name}
        return await self.request("POST", path, json=json)

    async def edit_role(
        self,
        server_id: str,
        role_id: str,
        *,
        name: Optional[str] = None,
        colour: Optional[str] = None,
        hoist: Optional[bool] = None,
        rank: Optional[int] = None,
        remove: Optional[Literal["Colour"]] = None,
    ):
        path = f"servers/{server_id}/roles/{role_id}"
        json = {"name": name}
        if colour:
            json["colour"] = colour
        if hoist:
            json["hoist"] = hoist
        if rank:
            json["rank"] = rank
        if remove:
            json["remove"] = remove
        return await self.request("PATCH", path, json=json)

    async def delete_role(self, server_id: str, role_id: str):
        path = f"servers/{server_id}/roles/{role_id}"
        return await self.request("DELETE", path)

    ##########
    ## Bots ##
    ##########

    async def create_bot(self, name: str) -> Response[Bot]:
        path = "bots/create"
        json = {"name": name}
        return await self.request("POST", path, json=json)

    async def get_owned_bots(self) -> Response[List[Bot]]:
        path = "bots/@me"
        return await self.request("GET", path)

    async def get_bot(self, bot_id: str) -> Response[Bot]:
        path = f"bots/{bot_id}"
        return await self.request("GET", path)

    async def edit_bot(
        self,
        bot_id: str,
        *,
        name: Optional[str] = None,
        public: Optional[bool] = None,
        interactions_url: Optional[str] = None,
        remove: Optional[Literal["InteractionsURL"]] = None,
    ):
        path = f"bots/{bot_id}"
        json = {}
        if name:
            json["name"] = name
        if public:
            json["public"] = public
        if interactions_url:
            json["interactionsURL"] = interactions_url
        if remove:
            json["remove"] = remove
        return await self.request("PATCH", path, json=json)

    async def delete_bot(self, bot_id: str):
        path = f"bots/{bot_id}"
        return await self.request("DELETE", path)

    async def get_public_bot(self, bot_id: str) -> Response[PublicBot]:
        path = f"bots/{bot_id}/invite"
        return await self.request("GET", path)

    async def invite_bot(
        self,
        bot_id: str,
        *,
        server_id: Optional[str] = None,
        group_id: Optional[str] = None,
    ):
        if server_id is None and group_id is None:
            raise ValueError("Either server_id or group_id must be provided")
        path = f"bots/{bot_id}/invite"
        json = {}
        if server_id:
            json["server"] = server_id
        if group_id:
            json["group"] = group_id
        return await self.request("POST", path)

    #############
    ## Invites ##
    #############

    async def get_invite(self, invite_id: str) -> Response[Invite]:
        path = f"invites/{invite_id}"
        return await self.request("GET", path)

    async def join_invite(self, invite_id: str) -> Response[JoinInvite]:
        path = f"invites/{invite_id}"
        return await self.request("POST", path)

    async def delete_invite(self, invite_id: str):
        path = f"invites/{invite_id}"
        return await self.request("DELETE", path)

    ##########
    ## Sync ##
    ##########

    async def get_settings(self, keys: List[str]) -> Response[Settings]:
        path = "sync/settings/fetch"
        json = {"keys": keys}
        return await self.request("POST", path, json=json)

    async def set_settings(self, settings: Dict[str, Any]):
        path = "sync/settings/set"
        return await self.request("POST", path, json=settings)

    async def get_unread(self) -> Response[Unreads]:
        path = "sync/unreads"
        return await self.request("GET", path)

    ##############
    ## Web Push ##
    ##############

    async def subscribe_web_push(
        self,
        endpoint: Any,
        p256d: Any,
        auth: Any,
    ):
        path = f"push/subscribe"
        json = {"endpoint": endpoint, "p256d": p256d, "auth": auth}
        return await self.request("PUT", path, json=json)

    async def unsubscribe_web_push(self, channel_id: str):
        path = f"push/unsubscribe"
        return await self.request("POST", path)
