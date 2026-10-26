;;; export.el --- export snellius-fs.org to beamer LaTeX  -*- lexical-binding: t; -*-
;; Org beamer turns *bold* into \alert; the deck uses \alert only where
;; the source asks for it, and plain bold everywhere else.
(require 'ox-beamer)
(defun snellius-fs-bold (_bold contents _info)
  (format "\\textbf{%s}" contents))
(advice-add 'org-beamer-bold :override #'snellius-fs-bold)
(org-beamer-export-to-latex)
