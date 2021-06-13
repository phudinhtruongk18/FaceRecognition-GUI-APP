import requests

url = 'https://api.fpt.ai/hmi/tts/v5'

payload = 'Phú đã điểm danh thành công'
headers = {
    'make_and_send-key': 'ojp4yPxFFpuNozefkke0ZrSQt5SXR55W',
    'speed': '',
    'voice': 'banmai'
}

response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)

print(response.text)