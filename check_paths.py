import os
print(f"CWD: {os.getcwd()}")
print(f"frontend/dist/index.html exists: {os.path.exists('frontend/dist/index.html')}")
print(f"frontend/dist/assets exists: {os.path.exists('frontend/dist/assets')}")
print(f"frontend entries: {os.listdir('frontend')}")
print(f"frontend/dist entries: {os.listdir('frontend/dist')}")
