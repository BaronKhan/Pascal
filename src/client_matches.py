clientMatches = [ {
					"Expression" : '("what" . "is" | "what\'s" | ["can" . "you"] . ["please"] . "tell" . "me") . "your" . "name" | "who" . "are" . "you"',
					"Result" : { "Intent" : "NAME" },
					"SpokenResponse" : "My name is pascal. Nice to meet you.",
					"SpokenResponseLong" : "My name is pascal. I am a robot who can be quite chatty. Nice to meet you.",
					"WrittenResponse" : "My name is pascal. Nice to meet you.",
					"WrittenResponseLong" : "My name is pascal. I am a robot who can be quite chatty. Nice to meet you."
				},
				{
					"Expression" : '["you" . ("can" | "may")] . ("shut" . "down" | "go" . "to" . "sleep" | "turn" . "off" | "terminate" | "close")',
					"Result" : { "Intent" : "SHUTDOWN" },
					"SpokenResponse" : "Shutting down.",
					"SpokenResponseLong" : "I am shutting down now. Goodbye.",
					"WrittenResponse" : "Shutting down.",
					"WrittenResponseLong" : "I am shutting down now. Goodbye."
				},
				{
					"Expression" : '("enter" | "start") . ("full" . "screen" | "fullscreen") . ["mode"] | "make" . ["the"] . "screen" . ("bigger" | "larger")',
					"Result" : { "Intent" : "FULLSCREEN_START" },
					"SpokenResponse" : "Fullscreen",
					"SpokenResponseLong" : "Entering fullscreen mode.",
					"WrittenResponse" : "Fullscreen",
					"WrittenResponseLong" : "Entering fullscreen mode."
				},
				{
					"Expression" : '("exit" | "stop") . ("full" . "screen" | "fullscreen") . ["mode"] | "make" . ["the"] . "screen" . ("smaller" | "tiny")',
					"Result" : { "Intent" : "FULLSCREEN_STOP" },
					"SpokenResponse" : "Fullscreen Ended.",
					"SpokenResponseLong" : "Exiting fullscreen mode.",
					"WrittenResponse" : "Fullscreen Ended.",
					"WrittenResponseLong" : "Exiting fullscreen mode."
				},
				{
					"Expression" : '"turn" . ("my" | "the") . ["bed"] . "lamp" . "on" | "switch" . "on" . ["the"] . ["bed"] . "lamp" | "activate" . ["the"] . ["bed"] . "lamp"',
					"Result" : { "Intent" : "LAMP_ON" },
					"SpokenResponse" : "Bed lamp on.",
					"SpokenResponseLong" : "Bed lamp activated.",
					"WrittenResponse" : "Bed lamp on.",
					"WrittenResponseLong" : "Bed lamp activated."
				},
				{
					"Expression" : '"turn" . ("my" | "the") . ["bed"] . "lamp" . "off" | "switch" . "off" . ["the"] . ["bed"] . "lamp" | "deactivate" . ["the"] . ["bed"] . "lamp"',
					"Result" : { "Intent" : "LAMP_OFF" },
					"SpokenResponse" : "Bed lamp off.",
					"SpokenResponseLong" : "Bed lamp deactivated.",
					"WrittenResponse" : "Bed lamp off.",
					"WrittenResponseLong" : "Bed lamp deactivated."
				} ]