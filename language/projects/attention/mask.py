import sys
import torch

from PIL import Image, ImageDraw, ImageFont
from transformers import AutoTokenizer, BertForMaskedLM

# Pre-trained masked language model
MODEL = "bert-base-uncased"

# Number of predictions to generate
K = 3

# Constants for generating attention diagrams
FONT = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 28)
GRID_SIZE = 40
PIXELS_PER_WORD = 200


def main():
    text = input("Text: ")

    # Tokenize input (use "pt" for PyTorch)
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    inputs = tokenizer(text, return_tensors="pt")
    
    mask_token_index = get_mask_token_index(tokenizer.mask_token_id, inputs)
    if mask_token_index is None:
        sys.exit(f"Input must include mask token {tokenizer.mask_token}.")

    # Use PyTorch model to process input
    model = BertForMaskedLM.from_pretrained(MODEL)
    result = model(**inputs, output_attentions=True)

    # Generate predictions using PyTorch torch.topk
    mask_token_logits = result.logits[0, mask_token_index]
    top_tokens = torch.topk(mask_token_logits, K).indices.tolist()
    for token in top_tokens:
        print(text.replace(tokenizer.mask_token, tokenizer.decode([token])))

    # Visualize attentions
    visualize_attentions(inputs.tokens(), result.attentions)


def get_mask_token_index(mask_token_id, inputs):
    """
    Return the index of the token with the specified `mask_token_id`, or
    `None` if not present in the `inputs`.
    """
    input_ids = inputs.input_ids[0].tolist()
    if mask_token_id in input_ids:
        return input_ids.index(mask_token_id)
    return None


def get_color_for_attention_score(attention_score):
    """
    Return a tuple of three integers representing a shade of gray for the
    given `attention_score`. Each value should be in the range [0, 255].
    """
    color = int(attention_score * 255)
    return (color, color, color)


def visualize_attentions(tokens, attentions):
    """
    Produce a graphical representation of self-attention scores.
    """
    # Iterate over each layer (i is 0-indexed)
    for layer_idx, layer_attention in enumerate(attentions):
        # Remove batch dimension: shape goes from (1, num_heads, seq_len, seq_len) -> (num_heads, seq_len, seq_len)
        heads = layer_attention[0]
        
        # Iterate over each head in the current layer (j is 0-indexed)
        for head_idx, head_attention in enumerate(heads):
            generate_diagram(
                layer_number=layer_idx + 1,
                head_number=head_idx + 1,
                tokens=tokens,
                attention_weights=head_attention
            )


def generate_diagram(layer_number, head_number, tokens, attention_weights):
    """
    Generate a diagram representing the self-attention scores for a single
    attention head.
    """
    image_size = GRID_SIZE * len(tokens) + PIXELS_PER_WORD
    img = Image.new("RGBA", (image_size, image_size), "black")
    draw = ImageDraw.Draw(img)

    for i, token in enumerate(tokens):
        token_image = Image.new("RGBA", (image_size, image_size), (0, 0, 0, 0))
        token_draw = ImageDraw.Draw(token_image)
        token_draw.text(
            (image_size - PIXELS_PER_WORD, PIXELS_PER_WORD + i * GRID_SIZE),
            token,
            fill="white",
            font=FONT
        )
        token_image = token_image.rotate(90)
        img.paste(token_image, mask=token_image)

        _, _, width, _ = draw.textbbox((0, 0), token, font=FONT)
        draw.text(
            (PIXELS_PER_WORD - width, PIXELS_PER_WORD + i * GRID_SIZE),
            token,
            fill="white",
            font=FONT
        )

    for i in range(len(tokens)):
        y = PIXELS_PER_WORD + i * GRID_SIZE
        for j in range(len(tokens)):
            x = PIXELS_PER_WORD + j * GRID_SIZE
            color = get_color_for_attention_score(attention_weights[i][j])
            draw.rectangle((x, y, x + GRID_SIZE, y + GRID_SIZE), fill=color)

    img.save(f"Attention_Layer{layer_number}_Head{head_number}.png")


if __name__ == "__main__":
    main()