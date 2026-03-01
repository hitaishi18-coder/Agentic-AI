import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

txt = "hey there! i am hitaishi "

tokens = enc.encode(txt)

print("tokens:-", tokens)

# tokens:- [48467, 1354, 0, 575, 939, 167343, 24597, 220]


decoded = enc.decode([48467, 1354, 0, 575, 939, 167343, 24597, 220])

print("decoded:-", decoded)