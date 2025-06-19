import React from "react";

export default function Cabeçalho(){
    return (
        <div className="min-h-screen bg-gray-100 font-sans text-gray-900 flex flex-col">
            <header className="bg-purple-800 text-white flex justify-between items-center px-6 py-4">
                <h1 className="flex items-center space-x-3 font-semibold text-lg">
                    <img src="images/image 16.png"></img>
                    <span>Smart City</span>
                </h1>

                <nav className="space-x-6 text-sm">
                    <a href="#about" className="hover:underline">About</a>
                    <a href="#dashboard" className="hover:underline">Dashboard</a>
                    <a href="#export" className="hover:underline">Export</a>
                </nav>

                <button
                aria-lebel="User profile"
                className="p-2 rounded-full bg-purple-700 hover:bg-purple-600"
                >

                <img className="bg-none" src="images/User.png"></img>

                </button>
            </header>
        </div>
    )
}