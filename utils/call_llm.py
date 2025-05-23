import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os

# Очистка кэша GPU перед загрузкой модели
if torch.cuda.is_available():
    print("🚀 Using GPU - clearing memory...")
    torch.cuda.empty_cache()
    print(f"[Память ДО загрузки] Allocated: {torch.cuda.memory_allocated()/1024**3:.2f} GB")

# Загружаем модель и токенизатор
MODEL_NAME = "TheBloke/Mistral-7B-Instruct-v0.1-GPTQ"
dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Инициализация модели с явным указанием truncation
print("\nЗагрузка токенизатора...")
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    truncation=True,  # Явное включение усечения
    model_max_length=512  # Максимальная длина контекста
)

print("\nЗагрузка модели...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    trust_remote_code=True,
    torch_dtype=torch.float16,
    revision="gptq-4bit-32g-actorder_True"
)
print(f"[Память ПОСЛЕ загрузки модели] Allocated: {torch.cuda.memory_allocated()/1024**3:.2f} GB")

# Создание пайплайна с дополнительными параметрами токенизации
print("\nСоздание пайплайна...")
generator = pipeline(
    "text-generation", 
    model=model, 
    tokenizer=tokenizer,
    truncation=True,  # Явное указание для пайплайна
)
print(f"[Память ПОСЛЕ создания пайплайна] Allocated: {torch.cuda.memory_allocated()/1024**3:.2f} GB")

def call_llm(prompt: str, max_tokens: int = 512) -> str:
    print(f"\nГенерация ответа... (до: {torch.cuda.memory_allocated()/1024**3:.2f} GB)")
    result = generator(
        prompt, 
        max_length=max_tokens,
        truncation=True,  # Явное указание при генерации
        do_sample=True, 
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id,
        num_return_sequences=1
    )[0]["generated_text"]
    print(f"[Память ПОСЛЕ генерации] Allocated: {torch.cuda.memory_allocated()/1024**3:.2f} GB")
    return result.replace(prompt, "").strip()