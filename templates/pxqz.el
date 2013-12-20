(defun pxqz-post ()
  (interactive)
  (let ((url-request-method "POST")
        (url-request-extra-headers
         '(("Content-Type" . "application/x-www-form-urlencoded")))
        (url-request-data
         (concat "t="
                 (buffer-string))))
    (url-retrieve "http://p.xqz.ca/" 'pxqz-handle-url)))

(defun pxqz-handle-url (status)
  (message "%s" (nth 1 status))
  (kill-new (current-message)))

(define-minor-mode pxqz-mode
  "Minor mode for easy pasting of buffers to p.xqz.ca"
  :lighter pxqz
  :keymap (let ((map (make-sparse-keymap)))
            (define-key map (kbd "C-x p") 'pxqz-post)
            map))
