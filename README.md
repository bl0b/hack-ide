Hack-IDE
============

* * * * *

 
## NAME

hackide - creates a persistent work environment in a terminal.  
## SYNOPSYS

**hackide** {-h|--help|help}
**hackide** description-file

**hackide files** description-file

**hackide templates**

 

## DESCRIPTION

When invoked with a single filename as argument, **hackide** builds
or restores a tmux session from a work-context description file
(see section **FILES** ). In a session, a number of tasks are laid
out in a single window by successively splitting panes. Each task
runs one command repetitively, so the command will respawn if it
quits. The tasks can define a number of resource files to store its
state and achieve persistence.
One can query the resource files related to a work-context by
putting **files** before the description filename.

**hackide** also defines task templates to simplify writing the
work-context description files. Invoke with the single argument
**templates** to view the existing templates, as well as the
template directory.

 

## FILES

 

### work-context description

This file contains three different types of lines :
context <context-name\>

This line defines the context name, which will become the tmux
session name.

task <name\> =\> <template\> [working-directory]
[command-parameters]

This line declares a task. **<name\>** may be followed (without
SPACES !) by a comma-delimited list of rc file definitions in the
form   
 "rc:<key\>:<filename\>". This will create an empty resource file by the name filename and this file can be mentioned in the command parameters by writing "%key%".

layout <layout-definition\>

A layout consists of either horizontal or vertical splits of the
terminal window. The syntax for a split is
**( <first\> <split-direction\> <size-of-second-pane-in-%\> <second\> )**
where *first* and *second* are either a task name or a split.
*split-direction* is **|** for an horizontal split or **--** for a
vertical split.

For instance, "(foo |50 (bar --50 baz))" creates a window with task
*foo* in the left half and task *bar* on top of task *baz* in the
right half.



**Example:**
    context test
    
    task editor => vim
    task sandbox,rc:pyhist:sandbox.pyhistory => cmd ./py PYHISTORY=%pyhist% python -i sandbox.py
    task shell => interactive_shell .
    
    layout ((sandbox --90 shell) |90 editor)

 

### task template

Task templates contain three types of directives :

RC <key\> <template\_filename\> (EMPTY|CONTENT)

Declares a resource file. When a task is created using this
template, the *template\_filename* is expanded using the dictionary
of the task, that is :
    {
            'T':task_name,
            'P':context_name,
            'PARAM':task_parameter_string,
            <any-rc-file-already-defined>
    }

If the last word is CONTENT, the file will be initialized from the
template expansion of all the following lines until the line "END
<key\> CONTENT", where <key\> is still the same.
CMD ...

Sets the command template. Whatever is on the right of the space
after "CMD" will be expanded using the task dictionary.

DOC

Starts the documentation bloc. This directive should appear only
once. The documentation is displayed when **hack-ide templates** is
invoked. Documentation ends with a line that contains "END DOC".

 

## TODO

Call context templates from the commandline.


 

## BUGS

Layouts with many windows don't work well. Some theoretically
equivalent layouts are not equivalent in practice.
Sometimes when killing an interpreter the pane will die too. Need
some \^D catching somewhere.  

## AUTHOR

Damien "bl0b" Leroux (damien.leroux (at) gmail.com)





* * * * *

 
## Index

[NAME](#lbAB)
[SYNOPSYS](#lbAC)
[DESCRIPTION](#lbAD)
[FILES](#lbAE)
[work-context description](#lbAF)
[task template](#lbAG)
[TODO](#lbAH)
[BUGS](#lbAI)
[AUTHOR](#lbAJ)

* * * * *

