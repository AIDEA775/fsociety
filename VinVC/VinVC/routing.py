from channels import include

channel_routing = [
    include('chat_room.routing.channel_routing', path=r'^/chat_room/'),
    include('friendship.routing.channel_routing', path=r'^/friendship/'),
    include('video_room.routing.channel_routing', path=r'^/video_room/'),
]

