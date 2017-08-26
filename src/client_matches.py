clientMatches = [ {
					"Expression" : '("what" . "is" | "what\'s" | ["can" . "you"] . ["please"] . "tell" . "me") . "your" . "name" | "who" . "are" . "you"',
					"Result" : { "Intent" : "NAME" },
					"SpokenResponse" : "My name is fir. Nice to meet you.",
					"SpokenResponseLong" : "My name is fir. I am a robot who can be quite chatty. Nice to meet you.",
					"WrittenResponse" : "My name is fir. Nice to meet you.",
					"WrittenResponseLong" : "My name is fir. I am a robot who can be quite chatty. Nice to meet you."
				},
				{
					"Expression" : '"shut" . "down" | "go" . "to" . "sleep" | "turn" . "off" | "terminate"',
					"Result" : { "Intent" : "SHUTDOWN" },
					"SpokenResponse" : "Shutting down.",
					"SpokenResponseLong" : "I am shutting down now. Goodbye.",
					"WrittenResponse" : "Shutting down",
					"WrittenResponseLong" : "I am shutting down now. Goodbye."
				} ]