import asyncio
from python.helpers import runtime, whisper, settings
from python.helpers.print_style import PrintStyle
import models

PrintStyle().print("Running preload...")
runtime.initialize()


async def preload():
    try:
        set = settings.get_settings()

        # preload whisper model
        async def preload_whisper():
            try:
                return await whisper.preload(set["stt_model_size"])
            except Exception as e:
                PrintStyle().error(f"Error in preload_whisper: {e}")

        # preload ollama models (已禁用)
        # async def preload_ollama_models():
        #     try:
        #         import subprocess
        #         import asyncio

        #         PrintStyle().standard("预热Ollama模型...")

        #         # 获取需要预热的模型列表
        #         models_to_warmup = []

        #         if set["chat_model_provider"] == models.ModelProvider.OLLAMA.name:
        #             models_to_warmup.append(set["chat_model_name"])

        #         if set["util_model_provider"] == models.ModelProvider.OLLAMA.name:
        #             models_to_warmup.append(set["util_model_name"])

        #         if set["embed_model_provider"] == models.ModelProvider.OLLAMA.name:
        #             models_to_warmup.append(set["embed_model_name"])

        #         # 去重
        #         models_to_warmup = list(dict.fromkeys(filter(None, models_to_warmup)))

        #         if not models_to_warmup:
        #             PrintStyle().standard("无需预热Ollama模型")
        #             return

        #         PrintStyle().standard(f"预热模型: {models_to_warmup}")

        #         # 并发预热所有模型
        #         async def warmup_single_model(model_name):
        #             try:
        #                 process = await asyncio.create_subprocess_exec(
        #                     'ollama', 'run', model_name, '你好',
        #                     stdout=asyncio.subprocess.PIPE,
        #                     stderr=asyncio.subprocess.PIPE
        #                 )
        #                 stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=60)

        #                 if process.returncode == 0:
        #                     PrintStyle().standard(f"✅ {model_name} 预热完成")
        #                 else:
        #                     PrintStyle().error(f"❌ {model_name} 预热失败: {stderr.decode()}")
        #             except asyncio.TimeoutError:
        #                 PrintStyle().error(f"⏰ {model_name} 预热超时")
        #             except Exception as e:
        #                 PrintStyle().error(f"❌ {model_name} 预热错误: {e}")

        #         # 并发执行预热
        #         await asyncio.gather(*[warmup_single_model(model) for model in models_to_warmup])
        #         PrintStyle().standard("Ollama模型预热完成")

        #     except Exception as e:
        #         PrintStyle().error(f"Error in preload_ollama_models: {e}")

        # preload embedding model
        async def preload_embedding():
            if set["embed_model_provider"] == models.ModelProvider.HUGGINGFACE.name:
                try:
                    emb_mod = models.get_huggingface_embedding(set["embed_model_name"])
                    emb_txt = await emb_mod.aembed_query("test")
                    return emb_txt
                except Exception as e:
                    PrintStyle().error(f"Error in preload_embedding: {e}")


        # async tasks to preload (ollama预热已禁用)
        tasks = [preload_whisper(), preload_embedding()]

        await asyncio.gather(*tasks, return_exceptions=True)
        PrintStyle().print("Preload completed")
    except Exception as e:
        PrintStyle().error(f"Error in preload: {e}")


# preload transcription model
asyncio.run(preload())
