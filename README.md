# TBX Ticket Tracker

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#technical-design-document">Technical Design Document (TDD)</a></li>
      </ul>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#docker">Docker</a></li>
        <li><a href="#vagrant">Vagrant</a></li>
      </ul>
    </li>
    <li><a href="#testing">Testing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## __About The Project__

**TBX Ticket Tracker**

This project is a simple CRUD application for tracking project tickets. User can create a Project, then create Tickets specific for each Project. Each Ticket can be assigned to several registered Users. Users can submit Comment to the Tickets. Users also have the ability to delete Project or Ticket. When a Project is deleted all Tickets in it will be removed from the system as well.

## __Technical Design Document (TDD)__
  ![tdd-diagram](https://github.com/jbhayback/tbx-ticket-tracker/blob/main/tbxcodingtask/static/images/tdd_tbx_tracker.png)
  - ### Use cases
    * User can view, create, update and delete Project.
    * User can view, create, update, and delete Ticket in a Project.
    * User can assign Ticket to several Users.
    * Users can submit Comments.
  - ### Additional feature(s)
    * On the Projects list, projects that the User has assigned tickets on should be shown above the other projects.

## Built With
* [Python](https://www.python.org/)
* [Django framework](https://www.djangoproject.com/)


## __Getting Started__

- ### Prerequisites
  - Docker and Docker Compose
    * [Docker](https://www.docker.com/)
      * [Installation](https://docs.docker.com/engine/install/)
    * [Docker compose](https://docs.docker.com/compose/)
      * [Installation](https://docs.docker.com/compose/install/)
  - [Vagrant](https://www.vagrantup.com/docs/installation)

- ### Docker

  Running the following commands will create your Docker container:

  ```bash
  cd tbx-ticket-tracker
  docker-compose up
  docker-compose exec web bash
  ```
  
  Then within the SSH session:
  
  ```bash
  python manage.py migrate
  python manage.py createcachetable
  python manage.py createsuperuser
  ```

  __IMPORTANT__: After performing the commands above, please restart all the containers to refresh the application.
  Failure to do this will not make the application to work.
  ```
  docker-compose down
  docker-compose up
  ```

  or Ctrl + C then
  ```
  docker-compose up
  ```


- ### Vagrant

  This repository includes a Vagrantfile for running the project in a Debian VM.
  
  Running the following commands will result in a local build of this project:
  
  ```bash
  cd tbx-ticket-tracker
  vagrant up
  vagrant ssh
  ```
  
  Then within the SSH session:
  
  ```bash
  dj migrate
  dj createcachetable
  dj createsuperuser
  djrun
  ```

## Testing
  - ### Unit Testing
    - You can run tests in the following way, Be sure the app's docker containers are up and running.
      ```bash
          docker-compose run web python ./manage.py test
      ```
  - ### Functional Testing
    - Access
        * http://localhost:8000/

## Contact
- You can contact me via email: jbhayback@gmail.com for more info or if there are errors during the setup.
