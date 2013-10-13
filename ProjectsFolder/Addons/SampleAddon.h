//
//  SampleAddon.h
//  iQTwist
//
//  Created by Jean-Francois Perusse on 13-07-06.
//

#import "CodeaAddon.h"

@interface SampleAddOn : NSObject<CodeaAddon>

static int _isRuntime(struct lua_State *state);
static int _getDeviceLanguage(struct lua_State *state);

@end
