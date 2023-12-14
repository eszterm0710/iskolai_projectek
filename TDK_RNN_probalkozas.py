import numpy as np
#numpyrandom seed
# Minta szöveg
text_data = """A mai zh angolul volt. 
Angolul nem tudok. 
Angol nem jó. PALI
"""
text_data_first=text_data[0]

# Szöveg előfeldolgozás
chars = list(set(text_data))
char_to_idx = {ch: i for i, ch in enumerate(chars)}
idx_to_char = {i: ch for i, ch in enumerate(chars)}
vocab_size = len(chars)

# Hiperparaméterek
hidden_size = 100
sequence_length = 30
learning_rate = 0.01

# Modell paraméterek inicializálása
Wxh = np.random.randn(hidden_size, vocab_size) * 0.01
Whh = np.random.randn(hidden_size, hidden_size) * 0.01
Why = np.random.randn(vocab_size, hidden_size) * 0.01
bh = np.zeros((hidden_size, 1))
by = np.zeros((vocab_size, 1))

# Képzés
def train():
    h_prev = np.zeros((hidden_size, 1))
    inputs = [char_to_idx[ch] for ch in text_data]
    targets = inputs[1:] + [char_to_idx['\n']]  # Következő karakter jóslása

    loss = 0
    dWxh, dWhh, dWhy = np.zeros_like(Wxh), np.zeros_like(Whh), np.zeros_like(Why)
    dbh, dby = np.zeros_like(bh), np.zeros_like(by)

    dhraw = np.zeros_like(h_prev)  # dhraw inicializálása

    for t in range(len(inputs)):
        x = np.zeros((vocab_size, 1))
        x[inputs[t]] = 1
        h = np.tanh(np.dot(Wxh, x) + np.dot(Whh, h_prev) + bh)
        y = np.dot(Why, h) + by
        p = np.exp(y) / np.sum(np.exp(y))
        loss += -np.log(p[targets[t], 0])

        dy = np.copy(p)
        dy[targets[t]] -= 1
        dWhy += np.dot(dy, h.T)
        dby += dy
        dh = np.dot(Why.T, dy) + np.dot(Whh.T, dhraw)
        dhraw = (1 - h * h) * dh
        dbh += dhraw
        dWxh += np.dot(dhraw, x.T)
        dWhh += np.dot(dhraw, h_prev.T)
        h_prev = h

    for dparam in [dWxh, dWhh, dWhy, dbh, dby]:
        np.clip(dparam, -2, 2, out=dparam)

    return loss, dWxh, dWhh, dWhy, dbh, dby

# Képzési loop
for iteration in range(1000):
    loss, dWxh, dWhh, dWhy, dbh, dby = train()
    for param, dparam in zip([Wxh, Whh, Why, bh, by], [dWxh, dWhh, dWhy, dbh, dby]):
        param -= learning_rate * dparam

    if iteration % 100 == 0:
        print(f"Iteration {iteration}, Loss: {loss}")

# Szöveggenerálás
def generate(seed, length=100, temperature=0.1):
    h = np.zeros((hidden_size, 1))
    x = np.zeros((vocab_size, 1))
    x[char_to_idx[seed]] = 1
    generated_text = seed

    for _ in range(length):
        h = np.tanh(np.dot(Wxh, x) + np.dot(Whh, h) + bh)
        y = np.dot(Why, h) + by
        p = np.exp(y) / np.sum(np.exp(y))
        next_char_idx = np.random.choice(range(vocab_size), p=p.ravel())
        next_char = idx_to_char[next_char_idx]
        generated_text += next_char
        x = np.zeros((vocab_size, 1))
        x[next_char_idx] = 1

    return generated_text

# Szöveggenerálás
generated_text = generate(text_data_first, length=500)
print(generated_text)