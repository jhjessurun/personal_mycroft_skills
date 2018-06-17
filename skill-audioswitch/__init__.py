# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.
__author__ = "jhjessurun"

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import getLogger
import subprocess

LOGGER = getLogger(__name__)

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.
class AudioSwitchSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(AudioSwitchSkill, self).__init__(name="AudioSwitchSkill")

        # Initialize working variables used within the skill.
        #self.host = '192.168.0.108'
        self.host =  'localhost'
        self.topic = 'switch/command'
        self.message = '1'

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #    vocab/en-us/Swich.voc
    #    vocab/en-us/Channel.voc
    # In this example that means it would match on utterances like:
    #   'Switch to'
    #   'Change to'

    @intent_handler(IntentBuilder("RandomSong").require("Randomize").require("Boolean"))
    def handle_randomize_intent(self,message):
        onoff=message.data.get("Boolean")
        if onoff==None:
           onoff="on"
        cmd=['mosquitto_pub','-h',self.host,'-t','switch/randomize','-m',onoff]
        try:
            subprocess.call(cmd)
            if (onoff=="on"):
                 self.speak("Switched play mode to randomized")
            else:
                 self.speak("Switched play mode to normal")
        except:
            self.speak("Sorry, some error occurred in AudioSwitch skill. Could not comply.")

    @intent_handler(IntentBuilder("BackForward").require("Goto").require("Direction").require("Entity"))
    def handle_goto_intent(self,message):
        direction=message.data.get("Direction")
        entity=message.data.get("Entity")
        cmd=['mosquitto_pub','-h',self.host,'-t','switch/'+entity,'-m',direction]
        subprocess.call(cmd)
        self.speak("Jumping to "+direction+" "+entity+".")

    @intent_handler(IntentBuilder("JumpSong").require("Jump").require("SongNumber"))
    def handle_jump_song_intent(self,message):
        #Send signal to Audioswitch to engage in USB mode and jump to song nr. x
        songnumber = message.data.get('SongNumber')
        cmd=['mosquitto_pub','-h',self.host,'-t','switch/jump','-m',songnumber]
        try:
            subprocess.call(cmd)
            self.speak("Jumping to song number "+songnumber)
        except:
            self.speak("Sorry, could not comply")



    @intent_handler(IntentBuilder("SwitchChannel").require("Switch").require("Channel"))
    def handle_switch_channel_intent(self, message):
	#Check to which channel the switch is
        #This should be in the Channel Dialog return
	#
        channel = message.data.get('Channel')
        if (channel == "Grammophone"):
             self.message='1'
        elif (channel == "CD 1"):
             self.message='2'
        elif (channel == "CD 2"):
             self.message='3'
        elif (channel == "Jack"):
             self.message='4'
        elif (channel == "USB"):
             self.message='5'
        elif (channel == "radio"):
             self.message = '6'
        else:
             self.message='0'
        cmd=['mosquitto_pub','-h',self.host,'-t',self.topic,'-m',self.message]
        try:
             subprocess.call(cmd)
             self.speak("I switched audio to "+channel)
        except:
             self.speak("I am sorry, could not send a message to audio switcher")


    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return AudioSwitchSkill()
