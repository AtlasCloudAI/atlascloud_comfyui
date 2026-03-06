from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKlingEffects:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                'atlas_client': ('ATLAS_CLIENT',),
                'image': ('STRING', {'default': '', 'tooltip': 'Image URL or Base64 encoding, in the format of data:image/png;base64,... '}),
                'effect_scene': (['firework_2026', 'glamour_photo_shoot', 'box_of_joy', 'first_toast_of_the_year', 'my_santa_pic', 'santa_gift', 'steampunk_christmas', 'snowglobe', 'ornament_crash', 'santa_express', 'instant_christmas', 'particle_santa_surround', 'coronation_of_frost', 'building_sweater', 'spark_in_the_snow', 'scarlet_and_snow', 'cozy_toon_wrap', 'bullet_time_lite', 'magic_cloak', 'balloon_parade', 'jumping_ginger_joy', 'bullet_time', 'c4d_cartoon_pro', 'pure_white_wings', 'black_wings', 'golden_wing', 'pink_pink_wings', 'venomous_spider', 'throne_of_king', 'luminous_elf', 'woodland_elf', 'japanese_anime_1', 'american_comics', 'guardian_spirit', 'swish_swish', 'snowboarding', 'witch_transform', 'vampire_transform', 'pumpkin_head_transform', 'demon_transform', 'mummy_transform', 'zombie_transform', 'cute_pumpkin_transform', 'cute_ghost_transform', 'knock_knock_halloween', 'halloween_escape', 'baseball', 'inner_voice', 'a_list_look', 'memory_alive', 'trampoline', 'trampoline_night', 'pucker_up', 'guess_what', 'feed_mooncake', 'rampage_ape', 'flyer', 'dishwasher', 'pet_chinese_opera', 'gallery_ring', 'muscle_pet', 'squeeze_scream', 'running_man', 'disappear', 'mythic_style', 'steampunk', 'c4d_cartoon', '3d_cartoon_1', '3d_cartoon_2', 'eagle_snatch', 'hug_from_past', 'firework', 'hug', 'kiss', 'heart_gesture', 'fight', 'emoji', "let's_ride", 'let’s_ride', 'snatched', 'magic_broom', 'felt_felt', 'jumpdrop', 'celebration', 'splashsplash', 'hula', 'surfsurf', 'fairy_wing', 'angel_wing', 'dark_wing', 'skateskate', 'plushcut', 'jelly_press', 'jelly_slice', 'jelly_squish', 'jelly_jiggle', 'pixelpixel', 'yearbook', 'instant_film', 'anime_figure', 'rocketrocket', 'bloombloom', 'dizzydizzy', 'fuzzyfuzzy', 'squish', 'expansion', 'santa_gifts', 'santa_hug', 'girlfriend', 'boyfriend', 'boylfriend', 'heart_gesture_1', 'pet_wizard', 'pet_lion', 'smoke_smoke', 'thumbs_up', 'pet_chef', 'pet_delivery', 'instant_kid', 'dollar_rain', 'cry_cry', 'building_collapse', 'gun_shot', 'mushroom', 'double_gun', 'pet_warrior', 'lightning_power', 'jesus_hug', 'magic_fireball', 'shark_alert', 'long_hair', 'lie_flat', 'polar_bear_hug', 'brown_bear_hug', 'jazz_jazz', 'office_escape_plow', 'offic_escape_plow', 'fly_fly', 'watermelon_bomb', 'pet_dance', 'boss_coming', 'wool_curly', 'iron_warrior', 'pet_moto_rider', 'pet_bee', 'marry_me', 'swing_swing', 'day_to_night', 'piggy_morph', 'wig_out', 'car_explosion', 'ski_ski', 'tiger_hug', 'siblings', 'construction_worker', 'media_interview'], {'default': 'firework_2026', 'tooltip': 'Effect scene'}),
            },
            "optional": {
                'poll_interval_sec': ('FLOAT', {'default': 2.0, 'min': 0.5, 'max': 10.0, 'tooltip': 'Polling interval (seconds)'}),
                'timeout_sec': ('INT', {'default': 900, 'min': 30, 'max': 7200, 'tooltip': 'Timeout (seconds)'}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        effect_scene: str,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required for AtlasCloud Kling Effects")

        effect_scene = (effect_scene or "").strip()
        if not effect_scene:
            raise RuntimeError("effect_scene is required for AtlasCloud Kling Effects")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "kwaivgi/kling-effects",
            "image": image,
            "effect_scene": effect_scene,
        }

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
