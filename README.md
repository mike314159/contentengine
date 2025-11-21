
Currently this works in both Digital Ocean App Plaftorm and Render.com.


On Render root directory under settings is set to "build/prod" and it seems to figure out that
the port is 5000. 

On DO source dir is set to "build/prod", but I also had to go in 
and set HTTP port to 5000 (in the UI) 
and modify the App Spec to set the dockerfile_path as follows. 

    services:
    - dockerfile_path: build/prod/Dockerfile
    github:
        branch: main
        repo: mike314159/flask-test
    http_port: 5000
    instance_count: 1
    instance_size_slug: basic-xxs
    name: flask-test
    source_dir: build/prod

