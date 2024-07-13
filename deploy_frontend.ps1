$ErrorActionPreference = "Stop"

try {
    Write-Host "- Start Frontend Deploy" -ForegroundColor Green

    # set location to this script dir
    Set-Location $PSScriptRoot

    # aws configure
    $credential = Get-Content "~/credential.yaml" | ConvertFrom-Yaml
    $env:AWS_ACCESS_KEY_ID = $credential.aws.iam.access_key_id
    $env:AWS_SECRET_ACCESS_KEY = $credential.aws.iam.secret_access_key
    $env:AWS_DEFAULT_REGION = $credential.aws.iam.region

    # config
    $deploy_settings = Get-Content "./deploy_settings.yaml" | ConvertFrom-Yaml
    $bucket = $deploy_settings.frontend.bucket
    $cloudfront_id = $deploy_settings.frontend.cloudfront_id

    Function Check {
        Param($status)
        if (-not $status) {
            throw "- Exeption happend"
        }
    }

    # build vue
    Set-Location ./frontend-vue
    Write-Host "- npm run build" -ForegroundColor Yellow
    npm run build
    Check $?

    # copy all object to s3
    Write-Host "- aws s3 cp ./dist $bucket --recursive" -ForegroundColor Yellow
    aws s3 cp ./dist $bucket --recursive
    Check $?

    # clear cache on cloudfront
    Write-Host "- aws cloudfront create-invalidation --distribution-id $cloudfront_id --paths '/*' --no-cli-pager" -ForegroundColor Yellow
    aws cloudfront create-invalidation --distribution-id $cloudfront_id --paths '/*' --no-cli-pager
    Check $?

    Write-Host "- Successfully Deployed" -ForegroundColor Green

} catch {
    Write-Host $Error[0] -ForegroundColor Red
    Write-Host $PSItem.ScriptStackTrace -ForegroundColor Red

} finally {
    Set-Location $PSScriptRoot
}
