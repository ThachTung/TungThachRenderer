#version 330 core

layout (location = 0) in vec2 inTexcoord;
layout (location = 1) in vec3 inNormal;
layout (location = 2) in vec3 inPosition;

out vec2 uv0;
out vec3 normal;
out vec3 fragPosition;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

void main ()
{
    uv0 = inTexcoord;
    fragPosition = vec3(model * vec4(inPosition,1.0));
    normal = mat3(transpose(inverse(model))) * normalize(inNormal);
    gl_Position = projection * view * model * vec4(inPosition, 1.0);
}