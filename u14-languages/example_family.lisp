;;; example_family.lisp: the family example as Lisp lists.
;;; Run: sbcl --script example_family.lisp
(defparameter *parents* '((ada bayo) (bayo chika) (bayo dayo)))

(defun children (p)
  (mapcar #'second
          (remove-if-not (lambda (pair) (eq (first pair) p)) *parents*)))

(defun grandchildren (p)
  (mapcan #'children (children p)))

(format t "grandchildren of ada: ~a~%" (grandchildren 'ada))
