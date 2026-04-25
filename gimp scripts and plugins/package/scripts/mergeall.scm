(define (script-fu-merge-all-layers) 
  (let* ((i (car (gimp-image-list))) 
         (image)) 
    (while (> i 0) 
      (set! image (vector-ref (cadr (gimp-image-list)) (- i 1))) 
      (gimp-image-merge-visible-layers image CLIP-TO-IMAGE)
      (set! i (- i 1))))) 

(script-fu-register "script-fu-merge-all-layers" 
 "<Image>/File/Merge ALL Layers" 
 "Merge all layers of each opened image" 
 "Adam Denault" 
 "Adam Denault" 
 "2023-2-12" 
 "" 
 )
