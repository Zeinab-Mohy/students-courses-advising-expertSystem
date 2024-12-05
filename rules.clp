(deftemplate course
   (slot id)
   (slot name)
   (multislot prerequisites))

(deftemplate student
   (slot id)
   (slot name)
   (multislot completedCourses))

(defrule enrollmentCourses
   ?student <- (student (id ?studentId) (name ?studentName) (completedCourses $?completedCourses))
   ?course <- (course (id ?courseId) (name ?courseName) (prerequisites $?prerequisites))
   (test (subsetp $?prerequisites $?completedCourses))      (test (not (member$ ?courseId $?completedCourses)))     =>
   (printout t ?studentName " can enroll in " ?courseName "." crlf))




