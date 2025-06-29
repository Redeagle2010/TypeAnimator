# File: src/typeanimator/typeanimator.py

import sys
import time
import re

class TypeAnimatorError(Exception):
    """Custom exception for TypeAnimator errors."""
    pass

class TypeAnimator:
    COLORS = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        'reset': '\033[0m'
    }

    SPEEDS = {
        'slow': 0.1,
        'normal': 0.05,
        'fast': 0.01
    }

    @classmethod
    def parse_colors(cls, text):
        """
        Parses color tags in the format !/color\! and returns a list of (text, color) tuples.
        Only text between !/color\! is colored.
        """
        if not isinstance(text, str):
            raise TypeAnimatorError("Text must be a string.")
        pattern = r'!\/(\w+)\\!(.*?)((?=!\/\w+\\!)|$)'
        result = []
        last_end = 0
        for match in re.finditer(pattern, text):
            start, end = match.span()
            # Text before colored part (no color)
            if start > last_end:
                result.append((text[last_end:start], cls.COLORS['reset']))
            color_name = match.group(1)
            colored_text = match.group(2)
            color_code = cls.COLORS.get(color_name, cls.COLORS['reset'])
            result.append((colored_text, color_code))
            last_end = end
        # Text after last colored part (no color)
        if last_end < len(text):
            result.append((text[last_end:], cls.COLORS['reset']))
        return result

    @classmethod
    def type_animation(cls, text, speed='normal', mode='char', file=sys.stdout):
        """
        Animates the output of text with optional color tags and speed/mode settings.
        """
        if not isinstance(text, str):
            raise TypeAnimatorError("Text must be a string.")
        if speed not in cls.SPEEDS:
            raise TypeAnimatorError(f"Invalid speed '{speed}'. Valid: {list(cls.SPEEDS.keys())}")
        if mode not in ('char', 'word', 'sentence'):
            raise TypeAnimatorError(f"Invalid mode '{mode}'. Valid: 'char', 'word', 'sentence'.")

        delay = cls.SPEEDS[speed]
        colored_parts = cls.parse_colors(text)
        for part, color in colored_parts:
            if mode == 'char':
                for char in part:
                    file.write(f"{color}{char}{cls.COLORS['reset']}")
                    file.flush()
                    time.sleep(delay)
            elif mode == 'word':
                words = part.split(' ')
                for word in words:
                    file.write(f"{color}{word}{cls.COLORS['reset']} ")
                    file.flush()
                    time.sleep(delay)
            elif mode == 'sentence':
                sentences = re.split(r'([.!?])', part)
                for i in range(0, len(sentences)-1, 2):
                    sentence = sentences[i] + sentences[i+1]
                    file.write(f"{color}{sentence}{cls.COLORS['reset']} ")
                    file.flush()
                    time.sleep(delay)
        file.write('\n')
        file.flush()