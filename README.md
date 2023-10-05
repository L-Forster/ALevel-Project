# ALevel-Project

PyGame project for Computer Science A Level.

![image](https://github.com/L-Forster/ALevel-Project/assets/120142008/b52e5476-c28e-4a56-9568-a235e831d15a)
![image](https://github.com/L-Forster/ALevel-Project/assets/120142008/e0d93422-9f2e-48e4-bacb-ddc7ad448833)
![image](https://github.com/L-Forster/ALevel-Project/assets/120142008/17a39cbc-3c9e-4866-8cd8-cc30b3c1c23b)


I used an Object-Oriented Approach. Defining classes for entities, dividing them into sub-classes for the player, enemy and collectables. I could then implement class-specific behaviours for each of these.
Gaussian noise is generated, and then a high-pass filter is applied in order to produce the areas of oil (which restrict the player's movement).

Enemies patrol the level in a rectangular path until they sight a player, at which they will ruthlessly hunt them. The enemy can pass through the oil, unrestricted, making it imperative for the player to try to not attract their attention.
