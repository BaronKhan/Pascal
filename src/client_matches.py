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
					"Expression" : '"who" . "is" . "your" . "master" | "who" . "do" . "you" . "obey"',
					"Result" : { "Intent" : "MASTER_WHO" },
					"SpokenResponse" : "Baron",
					"SpokenResponseLong" : "My master is Baron who currently lives in this room.",
					"WrittenResponse" : "Baron",
					"WrittenResponseLong" : "My master is Baron who currently lives in this room."
				},
				{
					"Expression" : '"do" . "the" . ("milkshake" | "milk" . "shake") | ["can" . "you"] . ["do" . "a"] . "dance"',
					"Result" : { "Intent" : "MILKSHAKE" },
					"SpokenResponse" : "No.",
					"SpokenResponseLong" : "Do I look like I can dance? No.",
					"WrittenResponse" : "No.",
					"WrittenResponseLong" : "Do I look like I can dance? No."
				} ]