# How to schedule the deployment

You can schedule the deployment through QGIS Deployment Toolbelt using a task scheduler.

## On Windows

1. Open the **Task Scheduler**

    ![Task scheduler](/static/task_scheduler_windows_app.png)

2. Click on **Create Task**

   ![Create_task](/static/task_scheduler_windows_create_task.png)

3. Fill in the **general information**

   Assign a name and set security options.

   ![General_information](/static/task_scheduler_windows_create_task_general.png)

4. **Launch condition**

   Define the conditions for launching the task: at login, once a day, once a week...

   ![Launch_condition](/static/task_scheduler_windows_create_task_trigger.png)

5. **Action** performed

   Define the action performed by the task. The action performed will be the execution of a program.
   Choose the path of the executable and remember to specify the launch folder.

   ![Action](/static/task_scheduler_windows_create_task_action.png)

   More parameters are available in the last tabs: **Conditions** and **Settings**

6. **Monitoring**

   ![Monitoring](/static/task_scheduler_windows_monitoring.png)

   On the home screen, you can see the tasks, their status, you can edit/start/delete... them.
