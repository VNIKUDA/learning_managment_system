<h1 align=center>Learning Management System (LMS)</h1>
<h3 align=center>Workspace for Education - Django</h3>
<div align=center>https://aleks.pythonanywhere.com/</div>
<br>

## Project Overview
The **Learning Management System (LMS)** is a web-based platform designed to manage courses, modules, lessons, users, completions, and grades. Bassicaly it is Google Classroom clone.

## Project Goals
The main goal of this project is to build a robust and scalable system for managing the educational courses, enabling users to interact with courses, manage lessons, and submit completions, with role-based access to certain features.

## Features

### 1. Home Page
- List of all user's courses.
![Знімок екрана (328)](https://github.com/user-attachments/assets/009ff34c-49a7-469f-9714-367be08d9e37)


### 2. Authentication System
- Registration for new account (student or teacher) and login for existing accounts.
![Знімок екрана (340)](https://github.com/user-attachments/assets/3d88b2fe-6bcf-47e2-8478-e9d4e18c96f8)
- User profiles with options to edit personal information.
![Знімок екрана (329)](https://github.com/user-attachments/assets/0ea0c788-1206-4999-8677-e63bf211af57)


### 3. Courses
- Students can join course by join code and leave course
- Teachers can create new course and manage owned courses.
- Administrators can create, edit, and delete courses.
![Знімок екрана (331)](https://github.com/user-attachments/assets/3dc0c01a-67b5-4cfd-af48-eab9980f634a)


### 4. Modules and Lessons
- Lessons may include text, materials, and tasks.
- Teacher can manage modules and lessons only for their course.
- Administrators can create, edit, and delete lessons.
![Знімок екрана (334)](https://github.com/user-attachments/assets/d6e045a5-077e-41f2-aa42-9340f1e7e1f1)

### 5. Completions & Grades
- Students can view and submit task completions.
- Teachers can view task completions and grade students completion.
- Administrators can view and edit all grades.
![Знімок екрана (337)](https://github.com/user-attachments/assets/fe3176c1-f151-41b3-b7c0-2a78a4e7e326)
![Знімок екрана (339)](https://github.com/user-attachments/assets/56b9f74a-1b2d-4200-8e52-9eae5c745607)

## Technical Requirements

- **Frontend**: HTML, Bootstrap
- **Backend**: Django, PostgreSQL

## Usage

- Users can register and log in to their accounts.
- Students can view and enroll in courses, complete completions, and check their grades.
- Teachers can create courses and modules, add lessons, and grade task completion.
- Administrators have full control over the platform and can manage users, courses, lessons, and grades.
