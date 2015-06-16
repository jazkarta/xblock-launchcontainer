# xblock-launchcontainer
Open edX XBlock to include Appsembler's external course Container launcher

# Installation
```
$ pip install -e git+https://github.com/jazkarta/xblock-launchcontainer.git@master:egg=launchcontainer
```
or add to your requires.txt
```
-e git+https://github.com/jazkarta/xblock-launchcontainer.git@master:egg=launchcontainer
```

Update your `lms.env.json` to add:
```
"ADDL_INSTALLED_APPS" : ["launchcontainer"]
```
and
```
"FEATURES": {
    "ALLOW_ALL_ADVANCED_COMPONENTS": true
}
```

# Usage

* In Studio, navigate to a Course, and select 'Advanced Settings' underneath the 
'Settings' dropdown menu.
* Under  'Advanced Module List' add 
```
["launchcontainer"] to the list of advanced modules
```



