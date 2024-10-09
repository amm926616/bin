import re

def reduce_time_from_lrc(file_path, reduction_seconds):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        modified_lines = []
        time_pattern = re.compile(r'\[(\d{2}):(\d{2}\.\d{2})\]')

        for line in lines:
            matches = time_pattern.findall(line)
            modified_line = line

            if matches:
                for match in matches:
                    minutes = int(match[0])
                    seconds = float(match[1])
                    total_seconds = minutes * 60 + seconds - reduction_seconds

                    # Calculate new minutes and seconds
                    new_minutes = int(total_seconds // 60)
                    new_seconds = total_seconds % 60

                    # Replace the time in the line with the adjusted time
                    new_time = f"[{new_minutes:02}:{new_seconds:05.2f}]"
                    old_time = f"[{match[0]}:{match[1]}]"
                    modified_line = modified_line.replace(old_time, new_time, 1)
            
            modified_lines.append(modified_line)

        # Write the modified content to a new file
        output_path = file_path.replace('.lrc', '_modified.lrc')
        with open(output_path, 'w', encoding='utf-8') as file:
            file.writelines(modified_lines)
        
        print(f"Time reduced by {reduction_seconds} seconds successfully. Modified file saved as '{output_path}'.")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    file_path = input("Enter the LRC file path: ").strip()
    reduction_seconds = float(input("Enter the number of seconds to reduce from each line: "))
    reduce_time_from_lrc(file_path, reduction_seconds)
