from openai	import OpenAI
#Initialize Clients
client	= OpenAI(api_key='OPENAI_API_KEY')
#Initialize	conversation history
messages	= [
				{"role":	"system",	"content":	"You	are	a	helpful	assistant."}

]
print("ChatGPT	Console	Chat	(type	'quit'	to	exit)")
print("-" * 50)
while True:
				
				user_input	= input("You:	")
				
				if user_input.lower()	== 'quit':
								print("Goodbye!")
								break
				
				messages.append({"role":	"user",	"content":	user_input})
				
				
				completion	= client.chat.completions.create(
								model="gpt-4o",
								messages=messages
				)
				
				
				assistant_message	= completion.choices[0].message.content
				
				
				messages.append({"role":	"assistant",	"content":	assistant_message})
				
				
				print(f"AI:	{assistant_message}\n")