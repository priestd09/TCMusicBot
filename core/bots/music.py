from core.bots.base import SkypeBot
import time
from core.commands.music import MusicCommand
import multiprocessing


class MusicBot(SkypeBot):

    """ Bot for playing music from skype chat.

    ChatCommand format: {delimeter}{owner} {command} {args}
    """
    def __init__(self):
        super(MusicBot, self).__init__(name="Skype MusicBot")

    def register_command_owner(self):
        """ Register chat command owner name
        """
        self.command_handler.register_owner("musicbot")

    def register_command_delimiter(self):
        """ Register chat command delimiter
        """
        self.command_handler.register_delimiter("@")

    def register_commands(self):
        """ Register the list of commands and callback functions
        """
        self.music_command = MusicCommand()

        # TODO make dicts into RegisteredCommand objects for better access/visibility, and behaviour
        commands = [
            {
                "help": {"obj": self, "func": "help", "accepts_args": False, "description": "this message", "aliases": []},
                "stop": {"obj": self.music_command, "func": "stop", "accepts_args": False, "description": "stop the music", "aliases": []},
                "skip": {"obj": self.music_command, "func": "skip", "accepts_args": False, "description": "skip the current track", "aliases": []},
                "list": {"obj": self.music_command, "func": "list", "accepts_args": False, "description": "list the current queue", "aliases": []},
                "playing": {"obj": self.music_command, "func": "currently_playing", "accepts_args": False, "description": "the currently playing song", "aliases": []},
                "volume": {"obj": self.music_command, "func": "change_volume", "accepts_args": True, "description": "set the system volume", "aliases": ["vol", "v"]},
                "clear": {"obj": self.music_command, "func": "clear", "accepts_args": False, "description": "clear the current queue", "aliases": []},
                "search": {"obj": self.music_command, "func": "search", "accepts_args": True, "description": "search {search term}, {optional index}", "aliases": ["s"]},
                "queue": {"obj": self.music_command, "func": "queue", "accepts_args": True, "description": "queue {search term}, {optional index}", "aliases": ["q"]}
            }
        ]

        self.command_handler.register(commands)

    def help(self):
        """ Command Callback function

        Returns:
            text (string): Formatted list of the registered commands for this bot.
        """
        text = "TC Music Bot, supported commands\n"
        text += "======================\n"
        text += "\n".join(self.command_handler.registered_commands())

        return text

    def run(self):
        """ Bot main run loop
        """
        while True:
            time.sleep(1.0)
            if len(self.queue) == 0:
                p = multiprocessing.Process(target=self.music_command.play_next, args=(self.queue,))
                p.start()

            # Set the currently playing flag based on whether there is a song currently playing.
            if self.queue:
                self.music_command.set_playing(True)
            else:
                self.music_command.set_playing(False)