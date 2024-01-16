# sm64 skybox adding script

a python script to add new skyboxes to an sm64 decomp project<br>
<br>
shoutouts to furyiousfight for making the [sm64 sfx importer](https://github.com/furyiousfight/HackerSM64-sfx-importer) which reminded me that I never actually released this script<br>
<br>
be sure to check her stuff out<br>

---

## usage

you should just be able to call the script with your skyboxes filename and it should automatically update the necessary files<br>
<br>
the script must be ran while your current directory is at the root of the decomp repo<br>
<br>
I recommend either putting the script in the `tools/` folder of your project and calling it like `./tools/add_skybox.py` or putting it somewhere your `PATH` environment variable points to and calling it like `add_skybox.py`<br>
<br>
you also might need to do `chmod +x add_skybox.py` to make it executable. if you dont want to do that, you can call the script through python like `python (path to script)`<br>

