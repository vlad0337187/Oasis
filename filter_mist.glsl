/* Mist filter. Can be runned at one time with internal mist.

Python Module can be used to control this shader in realtime (it'll change the owner object's properties.
(in oasis-1_v24.blend - for_filter_mist.py module)

Source: https://blenderartists.org/forum/showthread.php?358224-GLSL-Controllable-Mist
(26 Aug 2016)
*/

uniform sampler2D bgl_RenderedTexture;
uniform sampler2D bgl_DepthTexture;

uniform float dist;
uniform float density;

uniform float camNear; //camera clipping start
uniform float camFar; //camera clipping end
uniform float fov; //camera field of view
uniform float aspect; //camera aspect ratio

uniform float R;
uniform float G;
uniform float B;

uniform float model;
uniform float enable;
uniform float clipping;

float linearize(float depth)
{
    /**Some magic I pinched off Martinish's DOF shader
    I'm not entirely sure how it works, but without it, the mist is
    strange **/
	return -camFar * camNear / (depth * (camFar - camNear) - camFar);
}


float applyMist(float depth)
{
    /** Takes the depth and applies one of the mist models to it, either
    mixing it linearly, quadratically or exponential **/
    float factor = 0.0;
    if (model == 1.0){
        //Linear Mist
        factor = (depth-dist)/(density);
    } else if (model == 2.0){
        //Quadratic Mist
        factor = max(depth - dist, 0.0);
        factor = (factor * factor)/(density);
    } else if (model == 3.0){
        //Exponential Mist
        factor = 1.0 - exp(-(depth - dist)*density);
    }
    return factor;
}

float getDepth(float d_buffer)
{
    float depth = 1.0;
    depth = linearize(d_buffer);
    
    if (depth > camFar){
        //Clip the mist to allow for skyboxes
        depth = 0.0;
    }
    
    if (clipping < 1.5){
        //Mist plane
        depth = depth;
    } else {
        //Mist sphere
        float width = depth * tan(fov);
        float height = width / aspect;
        float y = (gl_TexCoord[0].st.y - 0.5) * 2.0 * height;
        float x = (gl_TexCoord[0].st.x - 0.5) * 2.0 * width;
        
        depth = length(vec3(x,y,depth));//pow(depth, 0.3333);
    }
    
    
        
    return depth;
}

void main() 
{
    vec4 dif = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);
    if (enable > 0.5){
        vec4 mist = vec4(R,G,B,0.0);
        
        float d_buffer = texture2D(bgl_DepthTexture,gl_TexCoord[0].xy).z;
        float depth = getDepth(d_buffer);
        float factor = applyMist(depth);
        
        gl_FragColor = mix(dif, mist, clamp(factor, 0.0, 1.0));
    } else {
        gl_FragColor = dif;
    }
}