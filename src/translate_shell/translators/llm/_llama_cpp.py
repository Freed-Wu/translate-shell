r"""LLaMa cpp
=============
"""
import os
from typing import Any

from llama_cpp import Llama

from ...external.platformdirs import AppDirs
from . import LLMTranslator

MODEL_PATH = str(AppDirs("translate-shell").user_data_path / "model.bin")
# cache init
old_model_path = MODEL_PATH
old_kwargs = {}
old_model = None


class LlamaTranslator(LLMTranslator):
    """Llamatranslator."""

    def __init__(self) -> None:
        """Init.

        :rtype: None
        """
        super().__init__("llama")

    @staticmethod
    def init_model(option: dict) -> Any:
        """Init model.

        :param option:
        :type option: dict
        :rtype: Any
        """
        global old_model_path, old_kwargs, old_model
        model_path = option.get("model", MODEL_PATH)
        if isinstance(model_path, Llama):
            # cache clear
            old_model_path = ""
            old_kwargs = {}
            old_model = model_path
            return model_path
        model_path = os.path.expanduser(model_path)
        kwargs = {}
        if n_ctx := option.get("n_ctx"):
            kwargs["n_ctx"] = int(n_ctx)
        if n_parts := option.get("n_parts"):
            kwargs["n_parts"] = int(n_parts)
        if n_gpu_layers := option.get("n_gpu_layers"):
            kwargs["n_gpu_layers"] = int(n_gpu_layers)
        if seed := option.get("seed"):
            kwargs["seed"] = int(seed)
        if f16_kv := option.get("f16_kv"):
            kwargs["f16_kv"] = bool(f16_kv)
        if logits_all := option.get("logits_all"):
            kwargs["logits_all"] = bool(logits_all)
        if vocab_only := option.get("vocab_only"):
            kwargs["vocab_only"] = bool(vocab_only)
        if use_mmap := option.get("use_mmap"):
            kwargs["use_mmap"] = bool(use_mmap)
        if use_mlock := option.get("use_mlock"):
            kwargs["use_mlock"] = bool(use_mlock)
        if embedding := option.get("embedding"):
            kwargs["embedding"] = bool(embedding)
        if n_threads := option.get("n_threads"):
            kwargs["n_threads"] = n_threads
        if n_batch := option.get("n_batch"):
            kwargs["n_batch"] = int(n_batch)
        if last_n_tokens_size := option.get("last_n_tokens_size"):
            kwargs["last_n_tokens_size"] = int(last_n_tokens_size)
        if lora_base := option.get("lora_base"):
            kwargs["lora_base"] = lora_base
        if lora_path := option.get("lora_path"):
            kwargs["lora_path"] = lora_path
        if low_vram := option.get("low_vram"):
            kwargs["low_vram"] = bool(low_vram)
        if tensor_split := option.get("tensor_split"):
            kwargs["tensor_split"] = tensor_split
        if rope_freq_base := option.get("rope_freq_base"):
            kwargs["rope_freq_base"] = float(rope_freq_base)
        if rope_freq_scale := option.get("rope_freq_scale"):
            kwargs["rope_freq_scale"] = float(rope_freq_scale)
        if verbose := option.get("verbose"):
            kwargs["verbose"] = bool(verbose)
        # cache hit
        if kwargs == old_kwargs and model_path == old_model_path and old_model:
            model = old_model
        else:
            model = Llama(model_path, **kwargs)
            # cache reinit
            old_model_path = model_path
            old_kwargs = kwargs
            old_model = model
        return model
