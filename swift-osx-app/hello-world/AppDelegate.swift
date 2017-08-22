//
//  AppDelegate.swift
//  hello-world
//
//  Created by Aravinth Panchadcharam on 20/10/16.
//  Copyright © 2016 Aravinth Panchadcharam. All rights reserved.
//

import Cocoa

@NSApplicationMain
class AppDelegate: NSObject, NSApplicationDelegate {

    @IBOutlet weak var label1: NSTextField!
    @IBOutlet weak var window: NSWindow!
    @IBOutlet weak var button1: NSButton!


    func applicationDidFinishLaunching(aNotification: NSNotification) {
        // Insert code here to initialize your application
        label1.stringValue = "Hello World"
        button1.title = "Hola"
    }

    func applicationWillTerminate(aNotification: NSNotification) {
        // Insert code here to tear down your application
    }

    @IBAction func changeLabel(sender: AnyObject) {
        label1.stringValue = "Hooola"
    }

}

