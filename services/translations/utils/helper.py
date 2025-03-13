import asyncio
import logging

from concurrent.futures import ThreadPoolExecutor, as_completed


logger = logging.getLogger(__name__)


class TranslationHelper:
    @staticmethod
    def translate_batch(provider_func, texts, from_lang, to_lang, batch_size, **kwargs):
        results = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                translated = provider_func.translate_texts(
                    batch,
                    from_language=from_lang,
                    to_language=to_lang,
                    **kwargs
                )
                results.extend(translated)
            except Exception as e:
                logger.error(f"Batch translation failed: {e}")
                results.extend([None] * len(batch))
        return results

    @staticmethod
    def translate_parallel(provider_func, texts, from_lang, to_lang, max_workers, **kwargs):
        results = [None] * len(texts)
        
        def _translate_task(index, text):
            try:
                return index, provider_func(
                    text,
                    from_language=from_lang,
                    to_language=to_lang,
                    **kwargs
                )
            except Exception as e:
                logger.error(f"Parallel translation failed for text {index}: {e}")
                return index, None

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(_translate_task, i, text)
                for i, text in enumerate(texts)
            ]
            
            for future in as_completed(futures):
                index, result = future.result()
                results[index] = result
                
        return results

    @staticmethod
    async def translate_async(provider_func, texts, from_lang, to_lang, **kwargs):
        async def _translate_async_task(text):
            try:
                return await provider_func(
                    text,
                    from_language=from_lang,
                    to_language=to_lang,
                    **kwargs
                )
            except Exception as e:
                logger.error(f"Async translation failed: {e}")
                return None

        tasks = [_translate_async_task(text) for text in texts]
        return await asyncio.gather(*tasks)