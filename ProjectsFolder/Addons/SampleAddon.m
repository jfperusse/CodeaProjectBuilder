//
//  SampleAddon.m
//  iQTwist
//
//  Created by Jean-Francois Perusse on 13-07-06.
//

#import "AppDelegate.h"
#import "CodeaViewController.h"
#import "SampleAddOn.h"
#import "lua.h"

static SampleAddOn *sampleAddOn;

@implementation SampleAddOn

+ (void) load
{
    [[NSNotificationCenter defaultCenter] addObserver:self
                                             selector:@selector(registerAddOn:)
                                                 name:@"RegisterAddOns"
                                               object:nil];
}

+ (void) registerAddOn:(NSNotification *)notification
{
    sampleAddOn = [[SampleAddOn alloc] init];
    CodeaViewController *viewController = (CodeaViewController*)[(AppDelegate*)[[UIApplication sharedApplication]delegate] viewController];
    [viewController registerAddon:sampleAddOn];
}

- (id)init
{
    self = [super init];
    if (self)
    {
        // Initialization stuff
    }
    return self;
}

- (void) codea:(CodeaViewController*)controller didCreateLuaState:(struct lua_State*)L
{
    NSLog(@"SampleAddOn Registering Functions");
    
    //  Register the functions, defined below
    
    lua_register(L, "_isRuntime", _isRuntime);
    lua_register(L, "_getDeviceLanguage", _getDeviceLanguage);
}

static int _isRuntime(struct lua_State *state)
{
    return 0;
}

static int _getDeviceLanguage(struct lua_State *state)
{
    NSString * language = [[NSLocale preferredLanguages] objectAtIndex:0];
    lua_pushstring(state, [language UTF8String]);
    return 1;
}

@end