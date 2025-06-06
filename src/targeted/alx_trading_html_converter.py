#!/usr/bin/env python3
"""
🌸✨ ALX Trading HTML Converter - Cute Data to HTML ✨🌸
Convert ALX trading data to beautiful HTML format
"""

import json
import html
from pathlib import Path
from datetime import datetime

class CuteAlxHtmlConverter:
    """Adorable HTML converter for ALX trading data"""
    
    def __init__(self):
        self.template_dir = Path("templates")
        self.output_dir = Path("data")
        self.template_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        print("🌸✨ ALX HTML Converter initialized! ✨🌸")
    
    def create_base_template(self):
        """Create beautiful base HTML template"""
        template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ALX Trading Data - {title}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(45deg, #ff6b6b, #ffeaa7);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px;
        }
        
        .message-item {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 5px solid #ff6b6b;
            transition: transform 0.3s ease;
        }
        
        .message-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .message-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px dashed #e9ecef;
        }
        
        .message-time {
            color: #6c757d;
            font-size: 0.9em;
            background: #e9ecef;
            padding: 5px 10px;
            border-radius: 20px;
        }
        
        .message-type {
            background: linear-gradient(45deg, #74b9ff, #0984e3);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .message-content {
            font-size: 1.1em;
            line-height: 1.6;
            color: #2d3436;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #2d3436;
        }
        
        .stat-label {
            color: #636e72;
            margin-top: 5px;
        }
        
        .footer {
            background: #2d3436;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .content {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌸 ALX Trading Data 🌸</h1>
            <p>{subtitle}</p>
        </div>
        
        <div class="content">
            {content}
        </div>
        
        <div class="footer">
            Generated on {timestamp} by Cute ALX HTML Converter 💖
        </div>
    </div>
</body>
</html>"""
        return template
    
    def format_messages_html(self, messages):
        """Format messages as HTML"""
        if not messages:
            return "<p>No messages found 😔</p>"
        
        html_content = ""
        
        # Add statistics
        stats_html = f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{len(messages)}</div>
                <div class="stat-label">Total Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(set(msg.get('user_id', 'unknown') for msg in messages))}</div>  
                <div class="stat-label">Unique Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(1 for msg in messages if msg.get('message_type') == 'text')}</div>
                <div class="stat-label">Text Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(1 for msg in messages if 'media' in msg.get('message_type', ''))}</div>
                <div class="stat-label">Media Messages</div>
            </div>
        </div>
        """
        
        html_content += stats_html
        
        # Add messages
        for i, message in enumerate(messages):
            timestamp = message.get('timestamp', 'Unknown')
            if isinstance(timestamp, (int, float)):
                try:
                    timestamp = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    timestamp = str(timestamp)
            
            content = html.escape(str(message.get('content', 'No content')))
            message_type = message.get('message_type', 'unknown')
            user_id = message.get('user_id', 'unknown')
            
            message_html = f"""
            <div class="message-item">
                <div class="message-header">
                    <div class="message-time">⏰ {timestamp}</div>
                    <div class="message-type">{message_type}</div>
                </div>
                <div class="message-content">
                    <strong>User:</strong> {user_id}<br>
                    <strong>Content:</strong> {content}
                </div>
            </div>
            """
            
            html_content += message_html
        
        return html_content
    
    def convert_json_to_html(self, json_file, output_file=None):
        """Convert JSON extraction file to HTML"""
        print(f"🔄 Converting {json_file} to HTML...")
        
        try:
            # Read JSON data
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Extract messages
            messages = []
            if isinstance(data, dict):
                if 'messages' in data:
                    messages = data['messages']
                elif 'data' in data:
                    messages = data['data']
                elif isinstance(data.get('extraction_results'), list):
                    messages = data['extraction_results']
                else:
                    # Try to find message-like data
                    for key, value in data.items():
                        if isinstance(value, list) and len(value) > 0:
                            if isinstance(value[0], dict) and ('content' in value[0] or 'text' in value[0]):
                                messages = value
                                break
            elif isinstance(data, list):
                messages = data
            
            if not messages:
                print("⚠️ No messages found in JSON file")
                messages = [{"content": "No message data found", "timestamp": "N/A", "message_type": "info"}]
            
            # Generate HTML
            template = self.create_base_template()
            content_html = self.format_messages_html(messages)
            
            # Fill template
            html_output = template.format(
                title="ALX Trading Messages",
                subtitle=f"Extracted messages from {Path(json_file).name}",
                content=content_html,
                timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            # Save HTML file
            if not output_file:
                json_path = Path(json_file)
                output_file = self.output_dir / f"{json_path.stem}.html"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_output)
            
            print(f"✅ HTML file created: {output_file}")
            return str(output_file)
            
        except Exception as e:
            print(f"💔 Error converting {json_file}: {e}")
            return None
    
    def batch_convert(self, input_dir="data", pattern="*.json"):
        """Batch convert multiple JSON files"""
        print(f"🔄 Batch converting JSON files from {input_dir}...")
        
        input_path = Path(input_dir)
        if not input_path.exists():
            print(f"💔 Input directory {input_dir} does not exist")
            return []
        
        json_files = list(input_path.glob(pattern))
        converted_files = []
        
        print(f"📁 Found {len(json_files)} JSON files to convert")
        
        for json_file in json_files:
            print(f"Processing: {json_file.name}")
            
            output_file = self.convert_json_to_html(json_file)
            if output_file:
                converted_files.append(output_file)
        
        print(f"🎉 Converted {len(converted_files)} files successfully!")
        return converted_files
    
    def create_index_page(self, html_files):
        """Create an index page linking to all HTML files"""
        print("📋 Creating index page...")
        
        # Create index content
        links_html = ""
        for html_file in html_files:
            file_path = Path(html_file)
            file_name = file_path.name
            file_size = file_path.stat().st_size if file_path.exists() else 0
            
            links_html += f"""
            <div class="message-item">
                <div class="message-header">
                    <div class="message-time">📄 {file_name}</div>
                    <div class="message-type">{file_size} bytes</div>
                </div>
                <div class="message-content">
                    <a href="{file_name}" style="color: #0984e3; text-decoration: none; font-weight: bold;">
                        🔗 Open {file_name}
                    </a>
                </div>
            </div>
            """
        
        # Generate index HTML
        template = self.create_base_template()
        index_html = template.format(
            title="ALX Trading Data Index",
            subtitle=f"Index of {len(html_files)} converted HTML files",
            content=f"<h2>📋 Available HTML Files</h2>{links_html}",
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        # Save index file
        index_file = self.output_dir / "index.html"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        print(f"✅ Index page created: {index_file}")
        return str(index_file)

def main():
    """Main conversion function"""
    print("🌸✨ ALX HTML Converter Starting! ✨🌸")
    
    converter = CuteAlxHtmlConverter()
    
    try:
        # Batch convert all JSON files
        converted_files = converter.batch_convert()
        
        if converted_files:
            # Create index page
            index_file = converter.create_index_page(converted_files)
            
            print(f"\n💖 Conversion Summary:")
            print(f"Files Converted: {len(converted_files)}")
            print(f"Index Page: {index_file}")
            print(f"\n🎉 Open the index.html file in your browser to view all data!")
        else:
            print("💔 No files were converted. Check if JSON files exist in data/ directory.")
            
    except Exception as e:
        print(f"💔 Conversion error: {e}")

if __name__ == "__main__":
    main()
