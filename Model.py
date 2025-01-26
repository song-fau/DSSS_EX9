import torch
from transformers import pipeline
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

pipe = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",  
    torch_dtype=torch.bfloat16,                
    device_map="auto"                           
)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hi, I'm your AI assistant. How can I help you?")

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  
    await update.message.reply_text("Please wait while I think...")  

    try:
        messages = [
            {
                "role": "system",
                "content": "You are a friendly chatbot who always responds in a helpful and engaging way.",
            },
            {"role": "user", "content": user_message},
        ]
        
 
        prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)


        outputs = pipe(
            prompt,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
        )
        response = outputs[0]["generated_text"]
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Sorry, an error occurred: {str(e)}")


def main():
 
    TOKEN = "7951231349:AAGOze0hFR8wTTjf56UuGvL-2tfrgK25hs8"
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) 

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
