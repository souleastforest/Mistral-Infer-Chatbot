import json
import requests
import textwrap

from qa_pairs import QAPairs


qa_pairs = QAPairs()
format_system_str = textwrap.dedent("""
    You are a professional code master. The task requirements are as follows:                     
    - Find errors in the JSON format and correct the format without modifying the content.
    - Ensure that all keys and values are properly quoted.
    - Validate that all nested structures are correctly closed.
    - Check for any trailing commas and remove them.
    - Ensure that the JSON is properly indented for readability.
    - Verify that all data types (strings, numbers, booleans) are correctly formatted.
""")

format_user_str = textwrap.dedent("""
    {
  "event1": {
    "Event name": "Enter the Enchanted Forest",
    "Event type": "Interactive Event",
    "Repeatable": false,
    "Trigger": {
      "Type": "Custom Intent",
      "Detail": "Player indicates readiness to enter the forest",
      "Role": "User"
    },
    "Actions": [
      {
        "action1": {
          "type": "Scene Change",
          "detail": "Transition from forest edge to dense, magical forest interior"
        }
      },
      {
        "action2": {
          "type": "Sound Effect Playback",
          "detail": "Mystical forest ambiance with whispers and ethereal sounds"
        }
      }
    ]
  },
  "event2": {
    "Event name": "Forest Path Choice",
    "Event type": "Interactive Event",
    "Repeatable": false,
    "Trigger": {
      "Type": "Other Event Completion",
      "Detail": "Enter the Enchanted Forest",
      "Role": "Character"
    },
    "Actions": [
      {
        "action1": {
          "type": "Scene Change",
          "detail": "Display three distinct paths in the misty forest"
        }
      },
      {
        "action2": {
          "type": "Motion Playback",
          "detail": "Character C kneels to examine tracks"
        }
      }
    ]
  },
  "event3": {
    "Event name": "Forest Sprites Encounter",
    "Event type": "Interactive Event",
    "Repeatable": false,
    "Trigger": {
      "Type": "Other Event Completion",
      "Detail": "Forest Path Choice",
      "Role": "Character"
    },
    "Actions": [
      {
        "action1": {
          "type": "Asset Loading",
          "detail": "Load and animate mischievous forest sprites"
        }
      },
      {
        "action2": {
          "type": "Sound Effect Playback",
          "detail": "Playful giggling and sounds of acorns hitting shields"
        }
      }
    ]
  },
  "event4": {
    "Event name": "Sprite Combat",
    "Event type": "Interactive Event",
    "Repeatable": false,
    "Trigger": {
      "Type": "Custom Intent",
      "Detail": "Player initiates combat or defensive action",
      "Role": "User"
    },
    "Actions": [
      {
        "action1": {
          "type": "Motion Playback",
          "detail": "Ushio raises shield, Character B casts spell, Character C shoots arrows"
        }
      },
      {
        "action2": {
          "type": "Sound Effect Playback",
          "detail": "Combat sounds, spell effects, and arrow impacts"
        }
      }
    ]
  },
  "event5": {
    "Event name": "Forest Guardian's Clearing",
    "Event type": "Interactive Event",
    "Repeatable": false,
    "Trigger": {
      "Type": "Other Event Completion",
      "Detail": "Sprite Combat",
      "Role": "Character"
    },
    "Actions": [
      {
        "action1": {
          "type": "Scene Change",
          "detail": "Transition to a mystical clearing with an ancient, gnarled tree"
        }
      },
      {
        "action2": {
          "type": "Asset Loading",
          "detail": "Load and animate the Forest Guardian character"
        }
      }
    ]
  },
  "event6": {
    "Event name": "Guardian's Test Initiation",
    "Event type": "Interactive Event",
    "Repeatable": false,
    "Trigger": {
      "Type": "Custom Intent",
      "Detail": "Player agrees to take the Guardian's test",
      "Role": "User"
    },
    "Actions": [
      {
        "action1": {
          "type": "Asset Loading",
          "detail": "Load three pedestals with symbols (sword, staff, bow)"
        }
      },
      {
        "action2": {
          "type": "Motion Playback",
          "detail": "Characters approach and place hands on their respective symbols"
        }
      }
    ]
  },
  "event7": {
    "Event name": "Shared Vision Quest",
    "Event type": "Interactive Event",
    "Repeatable": false,
    "Trigger": {
      "Type": "Other Event Completion",
      "Detail": "Guardian's Test Initiation",
      "Role": "Character"
    },
    "Actions": [
      {
        "action1": {
          "type": "Scene Change",
          "detail": "Transition to dreamlike version of the forest"
        }
      },
      {
        "action2": {
          "type": "Asset Loading",
          "detail": "Load illusionary beasts, magical riddles, and archery targets"
        }
      }
    ]
  },
  "event8": {
    "Event name": "Obtain Map of Elysiara",
    "Event type": "Mainline Event",
    "Repeatable": false,
    "Trigger": {
      "Type": "Other Event Completion",
      "Detail": "Shared Vision Quest",
      "Role": "Character"
    },
    "Actions": [
      {
        "action1": {
          "type": "Scene Change",
          "detail": "Return to Forest Guardian's clearing"
        }
      },
      {
        "action2": {
          "type": "Asset Loading",
          "detail": "Materialize the shimmering Map of Elysiara"
        }
      },
      {
        "action3": {
          "type": "Plot Switch",
          "detail": "Load next chapter"
        }
      }
    ]
  }
}
""")

gen_chapter_format_system = textwrap.dedent("""
    你是一个python编程语言大师，请按照用户的要求准确输出内容
"""),
output_prompt = textwrap.dedent("""
    {
  "Chapters": [
    {
      "Chapter Name": "The Call to Arms",
      "Chapter Title": "Chapter 1: Opening",
      "Appearing character": "Wise Mage (Character B)",
      "Chapter Introduction": "The game opens with Ushio Noa receiving the distressing news of the princess's abduction. As the kingdom's fate hangs in the balance, the player is introduced to the wise mage and skilled archer who offer their assistance. The chapter's focus is on the trio's initial meeting and the formation of their alliance. The player must choose their words and actions carefully to inspire trust and unity within the group.",
      "Chapter Game Objectives": "Form an alliance with the mage and archer."
    },
    {
      "Chapter Name": "Into the Enchanted Forest",
      "Chapter Title": "Chapter 2: Process",
      "Appearing character": "Skilled Archer (Character C)",
      "Chapter Introduction": "With their path set, the trio ventures into the heart of the Enchanted Forest. Here, they face their first set of challenges, encountering mystical creatures and solving enigmatic puzzles that require the unique skills of each member. Through these trials, the group's camaraderie begins to grow as they learn to work together and support each other.",
      "Chapter Game Objectives": "Defeat the Forest Guardian and obtain the Map of Elysiara."
    },
    {
      "Chapter Name": "The Trials of Unity",
      "Chapter Title": "Chapter 3: Climax",
      "Appearing character": "Ushio Noa",
      "Chapter Introduction": "As the group approaches the sorcerer's stronghold, they are forced to face their deepest fears and insecurities. A series of trials designed by the evil sorcerer tests the strength of their camaraderie. Overcoming these challenges will require Ushio to draw upon the collective wisdom and power of his companions.",
      "Chapter Game Objectives": "Complete the Trials of Unity and infiltrate the sorcerer's lair."
    },
    {
      "Chapter Name": "The Final Stand",
      "Chapter Title": "Chapter 4: Ending",
      "Appearing character": "Ushio Noa, Wise Mage (Character B), and Skilled Archer (Character C)",
      "Chapter Introduction": "The climax of the game sees the trio confronting the evil sorcerer in an epic battle. The strategic use of their combined abilities is the key to victory. Throughout the chapter, the deepened bond between the characters is reflected in their combat strategies and interactions, showcasing the power of camaraderie in the face of overwhelming adversity.",
      "Chapter Game Objectives": "Rescue the kidnapped princess and defeat the evil sorcerer."
    }
  ],
  "Game Title": "Sovereign Bonds of Valor",
  "Game Structure": "Structured gameplay.",
  "Setting Introduction": "Welcome to the mystical realm of Elysiara, where the fate of the kingdom rests in the hands of an unlikely trio. Ushio Noa, a young and inexperienced warrior, is propelled into a perilous journey by the sudden kidnapping of the beloved princess. Guided by the ancient wisdom of a wise mage (Character B) and bolstered by the unerring skill of a masterful archer (Character C), their quest will be fraught with danger, mystery, and discovery. The bond they forge along the way is not only essential to their survival but also to the future of Elysiara. As they traverse the treacherous Enchanted Forest, they must navigate the complexities of friendship, trust, and sacrifice to conquer the dark forces at play."
}
""")
gen_chapter_format_user = textwrap.dedent(f"""
这是我的剧情生成输入，请帮我将内容输出并转换格式为符合下面格式的内容：

剧情输入：
```
{output_prompt}
```

格式样例：
```
    - **Game Title**: "Example Game"
    - **Setting Introduction**: "This is a test setting."
    - **Game Structure**: "Structured gameplay."
    - **Chapter 1: Opening**:
        - **Chapter Name**: "Intro Chapter"
        - **Chapter Introduction**: "Introduction to the chapter."
        - **Chapter Game Objectives**: "Complete the intro."
        - **Appearing character**: "Character A"
    - **Chapter 2: Process**:
        - **Chapter Name**: "Middle Chapter"
        - **Chapter Introduction**: "Introduction to the middle chapter."
        - **Chapter Game Objectives**: "Complete the middle."
        - **Appearing character**: "Character B"
    - **Chapter 3: Climax**:
        - **Chapter Name**: "End Chapter"
        - **Chapter Introduction**: "Introduction to the end chapter."
        - **Chapter Game Objectives**: "Complete the end."
        - **Appearing character**: "Character C"
        ...
```
""")

json_format_prompt = qa_pairs.formatter(system_str=format_system_str, intent_message=format_user_str)
chapter_format_prompt = qa_pairs.formatter(gen_chapter_format_system, gen_chapter_format_user)

def log_token_usage(response):
    # 从response中提取usage信息
    usage_info = response.get("usage", {})
    completion_tokens = usage_info.get("completion_tokens", 0)
    prompt_tokens = usage_info.get("prompt_tokens", 0)
    total_tokens = usage_info.get("total_tokens", 0)

    # 记录或处理token使用情况
    print(f"Token usage - Completion: {completion_tokens}, Prompt: {prompt_tokens}, Total: {total_tokens}")

    # 如果需要，你也可以在这里执行其他逻辑，比如更新数据库中的token使用统计等
    return usage_info

import time

def test_api():
    url = "http://localhost:18000/v1/engines/completions"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral",
        # "prompt": chapter_format_prompt,
        # "prompt": json_format_prompt,
        "prompt": "Albert likes to surf every week. Each surfing session lasts for 4 hours and costs $20 per hour. How much would Albert spend in 5 weeks?",
        "max_tokens": 4096,
        "temperature": 0.35
    }

    start_time = time.time()
    response = requests.post(url, headers=headers, data=json.dumps(data))
    end_time = time.time()
    elapsed_time = end_time - start_time

    # 检查返回的状态码和输出
    if response.status_code == 200:
        raw_resp = response.json()
        content = raw_resp["choices"][0]["text"]
        usage = log_token_usage(raw_resp)
        print("API call successful")
        print("Raw Response:", json.dumps(raw_resp, indent=4, ensure_ascii=False))
        print(f"Content: {content.strip()}")
        print(f"Usage: {usage}")
    else:
        print("API call failed")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
    
    print(f"Request time: {elapsed_time:.2f} seconds")



if __name__ == "__main__":
    test_api()
