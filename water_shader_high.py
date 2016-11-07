##############################################################
# Water surface GLSL shader for BGE v1.0
# by Martins Upitis (martinsh) (devlog-martinsh.blogspot.com)
##############################################################

from bge import logic as g
from bge import render as r
import bgl

cont = g.getCurrentController()
own = cont.owner

VertexShader = """

attribute vec4 Tangent;
varying vec4 fragPos;
varying vec3 T, B, N; //tangent binormal normal
varying vec3 viewPos;
varying vec2 texCoord;

void main() 
{
	vec3 pos = vec3(gl_Vertex);
	
	T   = Tangent.xyz;
	B   = cross(gl_Normal, Tangent.xyz);
	N   = gl_Normal; 

    texCoord = gl_MultiTexCoord0.xy;
    fragPos = ftransform();
    viewPos = pos - gl_ModelViewMatrixInverse[3].xyz;
    gl_Position = ftransform();
}

"""

FragmentShader = """

varying vec4 fragPos; //fragment coordinates
varying vec3 T, B, N; //tangent binormal normal
varying vec3 viewPos;
varying vec2 texCoord;

uniform float timer;
uniform sampler2D reflectionSampler,refractionSampler,normalSampler;

//----------------
//tweakables

vec2 windDir = vec2(0.0, -0.5); //wind direction XY
float windSpeed = 0.9; //wind speed

float scale = 9500.0; //overall wave scale

/*vec2 bigWaves = vec2(0.6, 2.6); //strength of big waves, def: (2.0, 3.0)
vec2 midWaves = vec2(4.0, 2.0); //strength of middle sized waves, def: (4.0, 2.0)
vec2 smallWaves = vec2(3.0, 2.5); //strength of small waves, def: (1.0, 0.5)*/

vec2 bigWaves = vec2(0.1, 0.8);
vec2 midWaves = vec2(0.6, 0.2);
vec2 smallWaves = vec2(1.0, 0.2);

vec3 waterColor = vec3(0.25,0.3,0.45); //color of the water vec3(0.2,0.3,0.35)
float waterDensity = 0.9; //water density (0.0-1.0)
    
float choppy = 0.25; //wave choppyness // was 0.25
float aberration = 0.002; //chromatic aberration amount
float bump = 1.2; //overall water surface bumpyness
float reflBump = 0.3; //reflection distortion amount
float refrBump = 0.4; //refraction distortion amount

vec3 sunPos = vec3(500.0,500.0,200.0); //sun position
float sunSpec = 30.0; //Sun specular hardness

float scatterAmount = 1.0; //amount of sunlight scattering of waves
vec3 scatterColor = vec3(0.1,0.13,0.1);// color of the sunlight scattering
//----------------

vec3 tangentSpace(vec3 v)
{
	vec3 vec;
	vec.xy=v.xy;
	vec.z=sqrt(1.0-dot(vec.xy,vec.xy));
	vec.xyz= normalize(vec.x*T+vec.y*B+vec.z*N);
	return vec;
}

float fresnel_dielectric(vec3 Incoming, vec3 Normal, float eta)
{
    /* compute fresnel reflectance without explicitly computing
       the refracted direction */
    float c = abs(dot(Incoming, Normal));
    float g = eta * eta - 1.0 + c * c;
    float result;

    if(g > 0.0) {
        g = sqrt(g);
        float A =(g - c)/(g + c);
        float B =(c *(g + c)- 1.0)/(c *(g - c)+ 1.0);
        result = 0.5 * A * A *(1.0 + B * B);
    }
    else
        result = 1.0;  /* TIR (no refracted component) */

    return result;
}

void main() {
   
    vec2 fragCoord = (fragPos.xy/fragPos.w)*0.5+0.5;
    fragCoord = clamp(fragCoord,0.002,0.998);

	//normal map
	vec2 nCoord = vec2(0.0); //normal coords
 
  	nCoord = texCoord * (scale * 0.015) + windDir * timer * (windSpeed*0.03);
	vec3 normal0 = 2.0 * texture2D(normalSampler, nCoord + vec2(-timer*0.005,-timer*0.01)).rgb - 1.0;
	nCoord = texCoord * (scale * 0.05) + windDir * timer * (windSpeed*0.05)-normal0.xy*choppy;
	vec3 normal1 = 2.0 * texture2D(normalSampler, nCoord + vec2(+timer*0.01,+timer*0.005)).rgb - 1.0;
 
 	nCoord = texCoord * (scale * 0.15) + windDir * timer * (windSpeed*0.1)-normal1.xy*choppy;
	vec3 normal2 = 2.0 * texture2D(normalSampler, nCoord + vec2(-timer*0.02,-timer*0.03)).rgb - 1.0;
	nCoord = texCoord * (scale * 0.5) + windDir * timer * (windSpeed*0.2)-normal2.xy*choppy;
	vec3 normal3 = 2.0 * texture2D(normalSampler, nCoord + vec2(+timer*0.03,+timer*0.02)).rgb - 1.0;
  
  	nCoord = texCoord * (scale* 1.5) + windDir * timer * (windSpeed*1.0)-normal3.xy*choppy;
	vec3 normal4 = 2.0 * texture2D(normalSampler, nCoord + vec2(-timer*0.06,+timer*0.08)).rgb - 1.0;  
    nCoord = texCoord * (scale * 5.0) + windDir * timer * (windSpeed*1.3)-normal4.xy*choppy;
    vec3 normal5 = 2.0 * texture2D(normalSampler, nCoord + vec2(+timer*0.08,-timer*0.06)).rgb - 1.0;

	
	
	vec3 normal = normalize(normal0 * bigWaves.x + normal1 * bigWaves.y +
                            normal2 * midWaves.x + normal3 * midWaves.y +
						    normal4 * smallWaves.x + normal5 * smallWaves.y);

    //normal.x = -normal.x; //in case you need to invert Red channel
    //normal.y = -normal.y; //in case you need to invert Green channel
   
    vec3 nVec = tangentSpace(normal*bump); //converting normals to tangent space    
    vec3 vVec = normalize(viewPos);
    vec3 lVec = normalize(sunPos);
    //normal for light scattering
	vec3 lNormal = normalize(normal0 * bigWaves.x + normal1 * bigWaves.y*0.5 +
                            normal2 * midWaves.x*0.3 + normal3 * midWaves.y*0.3 +
						    normal4 * smallWaves.x*0.2 + normal5 * smallWaves.y*0.2);
    lNormal = tangentSpace(lNormal*bump);
    
	vec3 lR = reflect(lVec, lNormal);
	float s = max(dot(lR, vVec)*2.0-1.2, 0.0);
    float lightScatter = clamp((max(dot(-lVec,lNormal)*0.75+0.25,0.0)*s)*scatterAmount,0.0,1.0);
    
    
    //fresnel term
    float ior = 1.33;
    float eta = max(ior, 0.00001);
    float fresnel = fresnel_dielectric(vVec,nVec,eta);
   
    //texture edge bleed removal
    float fade = 12.0;
    vec2 distortFade = vec2(0.0);
    distortFade.s = clamp(fragCoord.s*fade,0.0,1.0);
    distortFade.s -= clamp(1.0-(1.0-fragCoord.s)*fade,0.0,1.0);
    distortFade.t = clamp(fragCoord.t*fade,0.0,1.0);
    distortFade.t -= clamp(1.0-(1.0-fragCoord.t)*fade,0.0,1.0); 
    
    vec3 reflection = texture2D(reflectionSampler, fragCoord+(nVec.st*reflBump*distortFade)).rgb;
    
    vec3 luminosity = vec3(0.30, 0.59, 0.11);
	float reflectivity = pow(dot(luminosity, reflection.rgb*2.0),3.0);
    
    vec3 R = reflect(vVec, nVec);

    float specular = pow(max(dot(R, lVec), 0.0),sunSpec)*reflectivity;

    vec2 rcoord = reflect(vVec,nVec).st;
    vec3 refraction = vec3(0.0);
    
    refraction.r = texture2D(refractionSampler, (fragCoord-(nVec.st*refrBump*distortFade))*1.0).r;
    refraction.g = texture2D(refractionSampler, (fragCoord-(nVec.st*refrBump*distortFade))*1.0-(rcoord*aberration)).g;
    refraction.b = texture2D(refractionSampler, (fragCoord-(nVec.st*refrBump*distortFade))*1.0-(rcoord*aberration*2.0)).b;
    
    
    vec3 Transmittance = mix(refraction,refraction*waterColor,waterDensity);

    vec3 color = mix(mix(Transmittance,scatterColor,lightScatter),reflection,clamp(fresnel,0.0,1.0));
    
    gl_FragColor = vec4(color+specular,1.0);
 
}
"""

mesh = own.meshes[0]
for mat in mesh.materials:
	shader = mat.getShader()
	if shader != None:
		if not shader.isValid():
			shader.setSource(VertexShader, FragmentShader, 1)
		shader.setAttrib(g.SHD_TANGENT)
		shader.setSampler('reflectionSampler',0)
		shader.setSampler('refractionSampler',1)
		shader.setSampler('normalSampler',2)
		shader.setUniform1f('timer',own['timer'])
		#shader.setSampler('diffuseSampler',3)
