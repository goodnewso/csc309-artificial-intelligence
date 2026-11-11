;;; courses.lisp: the same prerequisite knowledge in Common Lisp.
;;; Knowledge is a list of lists; code walks it recursively.
(defparameter *prereqs*
  '((csc309 csc203) (csc309 cos201) (cos201 cos102)
    (cos102 cos101) (csc203 mth101)))

(defun direct (course)                  ; courses needed immediately
  (loop for (c before) in *prereqs*
        when (eq c course) collect before))

(defun needs (course)                   ; all courses needed, recursively
  (let ((d (direct course)))
    (append d (loop for x in d append (needs x)))))

(format t "Before CSC309 you need: ~a~%" (needs 'csc309))
(format t "Number of courses: ~d~%" (length (needs 'csc309)))
