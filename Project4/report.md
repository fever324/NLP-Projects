###1. Problem or Task

Commedy TV shows are playing a very special part of people's life nowadays. The key to the success of commedy Tv shows is the level of funnies of the themselves. Our task is to use natural language processing technics to evaluate comedy script's funnies level. We may evaluate the funnies level on a scale of 10.   
One example from a popular show Big Bang Theory is the following   

*Raj: I don't like bugs, okay. They freak me out.  
Sheldon: Interesting. You're afraid of insects and women. Ladybugs must render you catatonic.*  

Clearly the second sentence is the laugh point. Our system will look into the context of the laugh point and may give the laugh point a funniess level of 8/10.

The reason we choose to investigate in this is because we love watching Big Bang Theory and it is the TV series that is making the most money. We want to look into something that can be potentially useful and practical.



###3. Data and Data Annotation

We will get all transcrips of every epsiode of a commedy TV show such as Big Bang Theory, which can be found at *https://bigbangtrans.wordpress.com*. Mark all laugh point with a label as well as a funny score associated with a label \<lp,9> using amazon's mechanical turk (9 means this laugh point has a funnies of 9 out 10). Since The score is subjective score, we may have 5 or more people rate the laugh point and take the average of them. Each turk is going to read through the transcript of one episode and rate the laughing points. 

For example, for the following transcript which is the first couple of lines in season 1 episode 2 of Big Bang Theory. The label are added after the turk's work.
  
*Leonard: There you go, Pad Thai, no peanuts.*

*Howard: But does it have peanut oil?*

*Leonard: Uh, I’m not sure, everyone keep an eye on Howard in case he starts to swell up.* ***\<lp,8>***

*Sheldon: Since it’s not bee season, you can have my epinephrine.* ***\<lp, 7>***

*Raj: Are there any chopsticks?*

*Sheldon: You don’t need chopsticks, this is Thai food.*

*Leonard: Here we go.*

*Sheldon: Thailand has had the fork since the latter half of the nineteenth century. Interestingly they don’t actually put the fork in their mouth, they use it to put the food on a spoon which then goes into their mouth.* **\<lp,3>**