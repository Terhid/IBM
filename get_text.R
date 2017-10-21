# test
# 
myArgs <- commandArgs(trailingOnly = TRUE)

#print(paste0("arg1 is ", myArgs[[1]], "arg2 is ", myArgs[[2]]))

get_text <- function(tweetUser = "realDonaldTrump", outputname = "tweets.txt"){
    
    twitter_lib_present = "twitteR" %in% rownames(installed.packages())
    if (!twitter_lib_present) { install.packages("twitteR") }
    library("twitteR")
    
    #---AuthenticationusingOAuth
    consumer_key<-"dK0DxmMOL8IZxLjJthJTbdoYl"
    consumer_secret<-"LawIrCsSNPVsf40eGyyQDl3f0voBhDCOeQdgXAefS4UqCFiAvk"
    access_token<-"4871473943-W4DoWihEupNFX2Rz786e43M0dJFSFM4pGvSxbKe"
    access_token_secret<-"01Lfa6rUkmIS13u8h3KwgTQSWu0CMWOYwTfxmxpW47WvX"
    
    setup_twitter_oauth(consumer_key,consumer_secret,
                        access_token,access_token_secret)
    tweetsUserTimeLine<-userTimeline(tweetUser, n=3200)
    
    # print list to text
    sink(outputname)
    print(tweetsUserTimeLine)
    sink()
}


get_text(tweetUser =  myArgs[[1]], outputname = myArgs[[2]])
