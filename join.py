#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 13:34:08 2023

@author: adam178
"""

from PIL import Image
import os
from time import sleep
from tkinter import filedialog


class Join:
    def __init__(self):
        self.dir = 'joined_images'
        self.folder_path = ''
        self.name_count = 1
        self.extension = 0

    def select_folder(self):
        self.folder_path = filedialog.askdirectory(initialdir = '.', title = 'Select a folder.')
        return self.folder_path
    
    def create_dir(self):
        dir = self.dir
        
        try:
            os.mkdir(self.dir)
        except OSError:
            print("The directory already existed $s " % dir)
        else:
            print("Successfully created the directory %s " % dir)   
            
    def rename(self, old_name):
        extension = '_' + str(self.extension) + '.jpg'
        new_name = os.path.join(str(self.dir), str(self.name_count) + str(extension))

        os.rename(old_name, new_name)
        
    def join_2(self, image1, image2):
        im1 = Image.open(image1)
        im2 = Image.open(image2)
    
        new_im = Image.new('RGB', (im1.width, im1.height + im2.height))
    
        new_im.paste(im1, (0, 0))
        new_im.paste(im2, (0, im1.height))
    
        pre_name = 'asdfasdf.jpg'
        new_im.save(pre_name)
        
        return pre_name
    
    def join_3(self, image1, image2, image3):
        im1 = Image.open(image1)
        im2 = Image.open(image2)
        im3 = Image.open(image3)
        
        new_im = Image.new('RGB', (im1.width, im1.height + im2.height + im3.height))
    
        new_im.paste(im1, (0, 0))
        new_im.paste(im2, (0, im1.height))
        new_im.paste(im3, (0, im1.height + im2.height))
    
        pre_name = "asdfasdf.jpg"
        new_im.save(pre_name)
        
        return pre_name
    
    def join_images(self):
        images = os.listdir(self.folder_path)
        images = [i for i in images if i.endswith('.jpg')]
        images.sort()
        
        #၂ နဲ့ ၃ နဲ့စားပြီးအကြွင်းကိုယူ
        check_factor_of2 = len(images) % 2
        check_factor_of3 = len(images) % 3
        
    # files အရေအတွက်ကိုပြပြီးတော့ မေးမယ်။
        number_pictures = len(images)
        print(f"\nThe number of pictures are {number_pictures}")
        method = input('\nDo you want to join by 2 or 3?(2/3) - pressing other keys will end the program: ')

    # method 2 and variables.
        if method == '2' and check_factor_of2 == 0:
            for i in range(0, len(images), 2):
                image1 = self.folder_path + '/' + images[i]
                image2 = self.folder_path + '/' + images[i+1]
                old_name = self.join_2(image1, image2)
                
                os.remove(image1)
                os.remove(image2)
                
                self.rename(old_name)

                self.name_count += 1

                
        elif method == '2' and check_factor_of2 == 1:
            theone = images.pop()
            theone = self.folder_path + '/' + theone
            for i in range(0, len(images), 2):
                image1 = self.folder_path + '/' + images[i]
                image2 = self.folder_path + '/' + images[i+1]
                old_name = self.join_2(image1, image2)     
                
                os.remove(image1)
                os.remove(image2)
                
                self.rename(old_name)
            
                self.name_count += 1
            
            self.rename(theone)


    # method 3 and variables.
        elif method == '3' and check_factor_of3 == 0:
            for i in range(0, len(images), 3):
                image1 = self.folder_path + '/' + images[i]
                image2 = self.folder_path + '/' + images[i+1]
                image3 = self.folder_path + '/' + images[i+2]
                old_name = self.join_3(image1, image2,image3)
                
                os.remove(image1)
                os.remove(image2)
                os.remove(image3)
                
                self.rename(old_name)

                self.name_count += 1
                
        elif method == '3' and check_factor_of3 == 1:
            theone = images.pop()
            theone = self.folder_path + '/' + theone 
            for i in range(0, len(images), 3):
                image1 = self.folder_path + '/' + images[i]
                image2 = self.folder_path + '/' + images[i+1]
                image3 = self.folder_path + '/' + images[i+2]
                old_name = self.join_3(image1, image2,image3)
                
                os.remove(image1)
                os.remove(image2)
                os.remove(image3)
                
                self.rename(old_name)

                self.name_count += 1
                
                
            self.rename(theone)
                
        
        elif method == '3' and check_factor_of3 == 2:
            second = images.pop()
            first = images.pop()
            for i in range(0, len(images), 3):
                image1 = self.folder_path + '/' + images[i]
                image2 = self.folder_path + '/' + images[i+1]
                image3 = self.folder_path + '/' + images[i+2]
                old_name = self.join_3(image1, image2,image3)
                            
                os.remove(image1)
                os.remove(image2)
                os.remove(image3)
                
                self.rename(old_name)

                self.name_count += 1
                
            old_name = self.join_2(first, second)
            self.rename(old_name)
            
            # တစ်ခြားဟာနှိပ်ရင် else ထွက်မယ်။
        else:
            print('\nYou ended the program.')

def join_process():
    jn = Join()
    jn.extension = extension
    print("\nThis program will only work for jpg images, so please format the pictures before using it.")
    sleep(1)

    folder_path = jn.select_folder()
    new_dir = input('\nDo you want to save the pictures to a "joined images" folder or replace the original folder?(new/replace):')
    if new_dir == 'new':
        jn.create_dir()
        jn.join_images()
    elif new_dir == 'replace':
        jn.dir = str(folder_path)
        jn.join_images()

extension = 0
run_again = ''
while run_again == '' or run_again == 'y' or run_again == 'Y':
    if __name__ == "__main__":
        while True:
            join_process()




        
        
        
        
        

    