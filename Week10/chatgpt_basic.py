from openai	import OpenAI
#Initialize	the	OpenAI client with your API	key
client	= OpenAI(api_key='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')
#Make a simple API call
completion	= client.chat.completions.create(
				model="gpt-4.1-mini",
				messages=[
								{"role":	"system",	"content":	"You	are	a	helpful	assistant."},
								{"role":	"user",	"content":	"Hello!	What	is	AI?"}
				]
)
#Print the response
print(completion.choices[0].message.content)