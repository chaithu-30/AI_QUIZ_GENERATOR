"""List and test available Gemini models"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("="*70)
print("AVAILABLE GEMINI MODELS")
print("="*70)

working_models = []

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        model_name = model.name
        print(f"\n✓ {model_name}")
        print(f"  Display: {model.display_name}")
        
        # Test if it actually works
        try:
            test_model = genai.GenerativeModel(model_name)
            response = test_model.generate_content("Say hi")
            print(f"  Status: WORKING ✓")
            print(f"  Test response: {response.text[:30]}")
            working_models.append(model_name)
        except Exception as e:
            print(f"  Status: ERROR - {str(e)[:50]}")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)

if working_models:
    print(f"\n✓ Found {len(working_models)} working model(s):\n")
    for i, model in enumerate(working_models, 1):
        print(f"  {i}. {model}")
    
    print(f"\n🎯 RECOMMENDED: Use '{working_models[0]}' in llm_quiz_generator.py")
    print(f"\n   Change line 29 to:")
    print(f"   model_name='{working_models[0]}'")
else:
    print("\n✗ No working models found!")
    print("  Check your API key at: https://aistudio.google.com/apikey")

print("\n" + "="*70)
